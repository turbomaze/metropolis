from flask import Flask, redirect, request, jsonify
from PIL import Image
from io import BytesIO
import base64
app = Flask(__name__)


@app.route('/')
def home():
    return redirect('http://github.com/turbomaze/metropolis', 301)

@app.route('/infer', methods=['GET', 'POST'])
def infer():
    if request.method == 'GET':
        return 'Post an image to this URL!'
    else:
        base64_img = request.form['img']
        img = Image.open(BytesIO(base64.b64decode(base64_img)))
        obj = [
            {
               "shape":"cube",
               "x":10,
               "y":0,
               "z":0,
               "l":1,
               "h":20,
               "w":20,
               "xRot":0,
               "yRot":0,
               "zRot":0,
               "r":1.0,
               "g":0.0,
               "b":0.0
            },
            {
               "shape":"cube",
               "x":0,
               "y":0,
               "z":10,
               "l":20,
               "h":20,
               "w":1,
               "xRot":0,
               "yRot":0,
               "zRot":0,
               "r":0.0,
               "g":0.0,
               "b":1.0
            },
            {
               "shape":"cube",
               "x":0,
               "y":0,
               "z":-10,
               "l":20,
               "h":20,
               "w":1,
               "xRot":0,
               "yRot":0,
               "zRot":0,
               "r":0.0,
               "g":0.0,
               "b":0.0
            },
            {
               "shape":"cube",
               "x":4,
               "y":5,
               "z":3,
               "l":1.2,
               "h":3,
               "w":2,
               "xRot":70,
               "yRot":20,
               "zRot":10,
               "r":0.7,
               "g":0.2,
               "b":0.9
            },
            {
               "shape":"cube",
               "x":-5,
               "y":4,
               "z":-2,
               "l":3,
               "h":0.8,
               "w":1.2,
               "xRot":30,
               "yRot":50,
               "zRot":0,
               "r":0.9,
               "g":0.0,
               "b":0.3
            }
        ]
        return jsonify(obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
