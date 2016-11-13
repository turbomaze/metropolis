import numpy as np
from Tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageTk
from metropolis import CubeProblem, PrismProblem
from mh import MH
from pso import PSO
from preprocess import clean


def render_particles(rt, dimensions, particles):
    # render all particles
    img = Image.new('RGB', dimensions, '#ffffff')
    draw = ImageDraw.Draw(img)
    w = 3
    for p in particles:
        x = dimensions[0] * p.pos[0]
        y = dimensions[1] * p.pos[1]
        draw.rectangle(
            [x-w, y-w, x+w, y+w],
            fill=(255, 0, 0)
        )

    tk_img = ImageTk.PhotoImage(img)
    label_image = Label(rt, image=tk_img)
    label_image.place(
        x=0, y=0,
        width=img.size[0],
        height=img.size[1]
    )
    rt.update()

def test001():
    dims = (400, 300)
    mins = [0, 0, 3]
    maxes = [20, 18, 8]
    root = Tk()
    root.geometry(str(dims[0]) + 'x' + str(dims[1]))

    # domain specific
    numBoxes = 2
    correct = [0., 0., 5.] + [14., 0., 5.]
    problem = CubeProblem(
        root, dims, numBoxes,
        mins*numBoxes, maxes*numBoxes,
        radius=20
    )
    correct_img = problem.get_image(correct)
    correct_img.save('../data/correct.bmp')

    swarm = PSO(
        zip(mins*numBoxes, maxes*numBoxes),
        problem.get_likelihood_func
    )
    first_guess = swarm.optimize(
        8, 80, correct_img,
        lambda x: render_particles(root, dims, x)
    )
    print 'First guess: ', first_guess
    print 'First score: ', np.linalg.norm(np.subtract(first_guess, correct))
    metropolis = MH(
        problem.get_next,
        problem.get_likelihood_func,
        problem.get_prior_prob,
        lambda x: problem.render(problem.get_image(x), x)
    )
    guess = metropolis.optimize(
        correct_img, first_guess, trials=80
    )

    im = problem.get_image(guess)
    im.save('../data/guess.bmp')
    print 'Guess: ', guess
    print 'Score: ', np.linalg.norm(np.subtract(guess, correct))

#This test the prism renderer.
def test002():
    dims = (400, 300)
    mins = [0, 0, 0, 3, 3, 3]
    maxes = [20, 8, 12, 12, 12, 12]
    root = Tk()
    root.geometry(str(dims[0]) + 'x' + str(dims[1]))

    # domain specific

    numBoxes = 1
    correct = [5., 0., 10., 3,7,7]
    problem = PrismProblem(
        root, dims, numBoxes,
        mins*numBoxes, maxes*numBoxes,
        radius=20
    )
    correct_img = problem.get_image(correct)
    correct_img.save('../data/correct.bmp')

    swarm = PSO(
        zip(mins*numBoxes, maxes*numBoxes),
        problem.get_likelihood_func
    )
    first_guess = swarm.optimize(
        10, 50, correct_img,
        lambda x: render_particles(root, dims, x)
    )
    print 'First guess: ', first_guess
    print 'First score: ', np.linalg.norm(np.subtract(first_guess, correct))
    


    metropolis = MH(
        problem.get_next,
        problem.get_likelihood_func,
        problem.get_prior_prob,
        lambda x: problem.render(problem.get_image(x), x)
    )

    # execution
    first_guess = problem.get_random_cube()
    guess = metropolis.optimize(
        correct_img, first_guess, trials=160
    )

    im = problem.get_image(guess)
    im.save('../data/guess.bmp')

    print guess
    print 'Score: ', np.linalg.norm(np.subtract(guess, correct))

test001()
