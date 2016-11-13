from flask import Flask, redirect, request, jsonify
from PIL import Image
from io import BytesIO
import base64
from metropolis.metropolis import CubeProblem
from metropolis.mh import MH
from metropolis.preprocess import clean
app = Flask(__name__)


@app.route('/')
def home():
    return redirect('http://github.com/turbomaze/metropolis', 301)


@app.route('/infer', methods=['GET', 'POST'])
def infer():
    if request.method == 'GET':
        return 'Post an image to this URL!'
    else:
        num_boxes = int(request.form['num_boxes'])
        base64_img = request.form['img']
        img = Image.open(BytesIO(base64.b64decode(base64_img)))
        img = img.convert('RGB')
        img = clean(img)

        problem = CubeProblem(
            None, (400, 300), num_boxes,
            mins=[0, 0, 0, 2]*num_boxes,
            maxes=[20, 8, 15, 10]*num_boxes,
            radius=20
        )
        black = MH(
            problem.get_next,
            problem.get_likelihood_func,
            problem.get_prior_prob,
            lambda x: x
        )
        first_guess = problem.get_random_cube()
        guess = black.optimize(
            img, first_guess, trials=100
        )
        obj = [
            {
                "shape": "cube",
                "x": guess[4*i],
                "y": guess[4*i+1],
                "z": guess[4*i+2],
                "l": guess[4*i+3],
                "h": guess[4*i+3],
                "w": guess[4*i+3],
                "xRot": 0,
                "yRot": 0,
                "zRot": 0,
                "r": 1.0,
                "g": 0.0,
                "b": 0.0
            } for i in range(0, num_boxes)
        ]

        return jsonify(obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
