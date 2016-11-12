import numpy as np
from Tkinter import Tk
from metropolis import SquareProblem
from mh import MH
from utils import draw_from_model
from PIL import Image, ImageDraw

if __name__ == '__main__':
    # gui
    dims = (400, 300)
    root = Tk()
    root.geometry(str(dims[0]) + 'x' + str(dims[1]))

    # domain specific
    default_side = 50
    default_color = (0, 0, 0)
    blur_radius = 20
    problem = SquareProblem(
        root, dims, default_side, default_color, blur_radius
    )
    correct = problem.get_square((100, 150), default_side, default_color)
    metropolis = MH(
        problem.get_next,
        problem.get_likelihood_func,
        problem.get_prior_prob,
        lambda x: problem.render(problem.get_image(x))
    )

    # execution
    first_guess = problem.get_random_square()
    guess = metropolis.optimize(correct, first_guess, trials=100)
    print 'Answer: ', correct
    print 'Guess: ', guess

    # render 3d from here
    im = Image.new('RGB', dims, '#ffffff')
    draw = ImageDraw.Draw(im)

    camera = np.matrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [15, 10, 30]
    ])
    model = [
        [20, (0, 0, 0), '#000000', 1],
        [7, (5, 0, 2), '#ff0000', 0]
    ]
    draw_from_model(draw, camera, model, fov=200)
    im.show()
