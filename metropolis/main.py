from Tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageTk
from metropolis import CubeProblem
from mh import MH
from pso import PSO


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

if __name__ == '__main__':
    # gui
    dims = (400, 300)
    root = Tk()
    root.geometry(str(dims[0]) + 'x' + str(dims[1]))

    # domain specific
    problem = CubeProblem(
        root, dims, mins=[0,0,3], maxes=[20,20,7], radius=20
    )
    correct = [15., 5., 5]
    # swarm = PSO(
    #     [[0, 20], [0, 20]],
    #     problem.get_likelihood_func
    # )
    # swarm.optimize(
    #     10, 20, correct,
    #     lambda x: render_particles(root, dims, x)
    # )

    metropolis = MH(
        # problem.get_next,
        lambda x, y: problem.get_random_cube(),
        problem.get_likelihood_func,
        problem.get_prior_prob,
        lambda x: problem.render(problem.get_image(x))
    )

    # execution
    first_guess = problem.get_random_cube()
    guess = metropolis.optimize(correct, first_guess, trials=100)
    print 'Answer: ', correct
    print 'Guess: ', guess
