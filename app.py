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
        return jsonify(username='igliu')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
