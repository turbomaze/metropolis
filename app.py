from flask import Flask, redirect, request, jsonify
from PIL import Image
from io import BytesIO
import numpy as np
import base64
from metropolis.metropolis import CubeProblem
from metropolis.mh import MH
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
        r, g, b, a = img.split()
        problem = CubeProblem(
            None, (400, 300),
            mins=[0, 0, 5], maxes=[20, 20, 12],
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
            img, first_guess, trials=200
        )
        return jsonify(params=guess)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
