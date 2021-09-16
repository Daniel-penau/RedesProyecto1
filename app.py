import random
import time
import ffmpeg_methods as methods
from flask import Flask, render_template, request, send_from_directory
import os
import string
import binascii
import shutil

app = Flask(__name__)

def get_req_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/methods/images_to_video', methods=['POST'])
def images_to_video():
    files = request.files.getlist('files')
    response = {"status": "OK", "url": "example"}
    req_id = get_req_id()
    os.makedirs(os.path.join("temp", req_id))
    for file in files:
        file.save(os.path.join("temp", req_id, file.filename))
    methods.image_to_video(req_id)
    shutil.rmtree(os.path.join("temp", req_id))
    return response

@app.route('/methods/extract_audio', methods=['POST'])
def extract_audio():
    file = request.files.get("files")
    req_id = get_req_id()
    os.makedirs(os.path.join("temp", req_id))
    file.save(os.path.join("temp", req_id, file.filename))
    methods.extract_audio(req_id, file.filename)
    shutil.rmtree(os.path.join("temp", req_id))
    print("Sending: " + os.path.join("output", req_id + ".mp3"))
    return send_from_directory(os.path.join("output"), req_id + ".mp3", as_attachment=True)

@app.route('/methods/resize_video', methods=['POST'])
def resize_video():
    file = request.files.get("files")
    width = request.form.get("width")
    height = request.form.get("height")
    req_id = get_req_id()
    os.makedirs(os.path.join("temp", req_id))
    file.save(os.path.join("temp", req_id, file.filename))
    methods.resize_video(req_id, file.filename, int(width), int(height))
    shutil.rmtree(os.path.join("temp", req_id))
    print("Sending: " + os.path.join("output", req_id + ".mp4"))
    return send_from_directory(os.path.join("output"), req_id + ".mp4", as_attachment=True)

@app.route('/methods/trim_video', methods=['POST'])
def trim_video():
    file = request.files.get("files")
    start_time = request.form.get("start")
    end_time = request.form.get("end")
    req_id = get_req_id()
    os.makedirs(os.path.join("temp", req_id))
    file.save(os.path.join("temp", req_id, file.filename))
    methods.trim_video(req_id, file.filename, int(start_time), int(end_time))
    shutil.rmtree(os.path.join("temp", req_id))
    print("Sending: " + os.path.join("output", req_id + ".mp4"))
    return send_from_directory(os.path.join("output"), req_id + ".mp4", as_attachment=True)

@app.route('/methods/video_frames', methods=['POST'])
def video_frames():
    file = request.files.get("files")
    req_id = get_req_id()
    os.makedirs(os.path.join("temp", req_id))
    file.save(os.path.join("temp", req_id, file.filename))
    methods.frames_per_sec(req_id, file.filename)
    shutil.rmtree(os.path.join("temp", req_id))
    print("Sending: " + os.path.join("output", req_id + ".zip"))
    return send_from_directory(os.path.join("output"), req_id + ".zip", as_attachment=True)

if __name__ == '__main__':
    app.run()
