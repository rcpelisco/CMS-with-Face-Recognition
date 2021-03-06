from flask import Blueprint, render_template, jsonify
from flask import redirect, request, Response, url_for
from res.face_recognition import VideoCamera, Trainer
from ..site.extra import post

module = Blueprint('face_recognition', __name__, template_folder='templates')

@module.route('/')
def index():
    return render_template('face_recognition/index.html')

def detect(camera, with_name=True):
    while True:
        data = camera.detect(with_name)
        if(data['frames'] == 10 and with_name):
            post('/api/face_recognition/', {'name': data['patient'], 'fresh': 1})
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data['image'] + b'\r\n\r\n')

def record(camera):
    while True:
        data = camera.detect(with_name=False, record=True)
        if data['frames'] == 20:
            post('/api/face_recognition/', {'name': 'new-face', 'fresh': 1})
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data['image'] + b'\r\n\r\n')

def profile_picture_cap(camera):
    while True:
        data = camera.detect(with_name=False, capture=True)
        if data['frames'] == 1:
            post('/api/face_recognition/', {'name': data['image_path'], 'fresh': 1})
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data['image'] + b'\r\n\r\n')

@module.route('/show')
def show():
    return Response(detect(VideoCamera(), False),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@module.route('/recognize')
def recognize():
    return Response(detect(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@module.route('/recognize_user')
def recognize_user():
    return Response(detect(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@module.route('/collect/<name>')
def collect(name):
    return Response(record(VideoCamera(name)),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@module.route('/profile_picture/<name>')
def profile_picture(name):
    print(name)
    return Response(profile_picture_cap(VideoCamera(name)),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@module.route('/train')
def train():
    print('training')
    trainer = Trainer()
    trainer.train()
    return jsonify({'message': 'Done'})