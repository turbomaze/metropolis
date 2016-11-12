from flask import Flask, redirect, request, jsonify
from PIL import Image
from io import BytesIO
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
        img = img.convert('RGB')
        num_boxes = 1
        problem = CubeProblem(
            None, (400, 300), num_boxes,
            mins=[0, 0, 2], maxes=[20, 15, 10],
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
        obj = []
        for i in range (0, num_boxes):
          obj.append({
           "shape":"cube",
           "x":guess[3*i],
           "y":0,
           "z":guess[3*i+1],
           "l":guess[3*i+2],
           "h":guess[3*i+2],
           "w":guess[3*i+2],
           "xRot":0,
           "yRot":0,
           "zRot":0,
           "r":1.0,
           "g":0.0,
           "b":0.0
          })

        return jsonify(obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
