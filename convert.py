from flask import Blueprint, render_template, url_for, request, session, redirect, Response, render_template_string, send_file
from urllib.parse import urlparse
import sys
import os
import csv
import subprocess
convert = Blueprint('convert', __name__, template_folder='templates')


@convert.route('/get_link', methods =["GET", "POST"])
def start():
    files_list = os.listdir("dl/")
    print(str(len(files_list)), file=sys.stderr)
    if len(files_list) > 4:
        return render_template('convert.html', mode="too_many_files")
    if request.form.get("action") == "set_link":
        url = str(request.form.get("yt-url"))
        if not url or not is_valid_url(url):
            return "Invalid URL", 400
        session["link"] = url
        return render_template('convert.html', mode="download")
    return render_template('convert.html', mode="get_link")

@convert.route('/files', methods =["GET", "POST"])
def files():
    files_list = os.listdir("dl/")
    if request.form.get("action") == "delete_files":
        for list_files_i in files_list:
            os.remove("dl/"+list_files_i)
    files_list = os.listdir("dl/")
    return render_template('downloads.html', files=files_list)

@convert.route('/files/<filename>')
def get_file(filename):
    return send_file("dl/"+filename, as_attachment=True)

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False
        if not parsed.netloc.endswith(("youtube.com", "youtu.be", "vimeo.com")):
            return False
        return True
    except Exception:
        return False


@convert.route('/stream')
def stream():
    download_url = session.get('link')
    def generate():
        process = subprocess.Popen(
            #yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=oHg5SJYRHA0"
            ["/usr/local/bin/yt-dlp", "-vU", "-P dl/", "--extract-audio", "--audio-format", "mp3", "--audio-quality", "0", download_url],
            #["yt-dlp", download_url, "-P dl/", "--extract-audio --audio-quality 0 --audio-format mp3"],
            #["yt-dlp", "https://www.youtube.com/watch?v=kUT6ZhFdLkA"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1, shell=False
        )
        for line in iter(process.stdout.readline, ''):
            yield f"data: {line.rstrip()}\n\n"
        process.stdout.close()
        process.wait()
        # <<< when finished, send special DONE message
        yield "data: __DONE__\n\n"
    return Response(generate(), mimetype='text/event-stream')
