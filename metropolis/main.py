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

numBoxes = 1
dims = (400, 300)
mins = [0, 0, 0, 2]
maxes = [20, 8, 12, 12]
root = Tk()
root.geometry(str(dims[0]) + 'x' + str(dims[1]))

# domain specific
problem = CubeProblem(
    root, dims, numBoxes,
    mins*numBoxes, maxes*numBoxes,
    radius=20
)
correct = [15., 0., 10., 7]
correct_img = problem.get_image(correct)
correct_img.save('../data/correct.bmp')
metropolis = MH(
    problem.get_next,
    problem.get_likelihood_func,
    problem.get_prior_prob,
    lambda x: problem.render(problem.get_image(x), x)
)

# execution
first_guess = problem.get_random_cube()
guess = metropolis.optimize(
    correct_img, first_guess, trials=200
)

im = problem.get_image(guess)
im.save('../data/guess.bmp')

print guess
