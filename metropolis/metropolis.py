import random
import numpy as np
from mh import MH
from Tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageFilter, ImageTk


def render(img):
    blurred = img.filter(
        ImageFilter.GaussianBlur(radius=blur_radius)
    )

    tk_img = ImageTk.PhotoImage(blurred)
    label_image = Label(root, image=tk_img)
    label_image.place(
        x=0, y=0,
        width=img.size[0],
        height=img.size[1]
    )
    root.update()


def get_image(polygon):
    data = np.zeros((dims[1], dims[0], 3), dtype=np.uint8)
    data.fill(255)
    img = Image.fromarray(data, 'RGB')
    draw = ImageDraw.Draw(img, 'RGB')
    draw.polygon(polygon['points'], polygon['color'])
    del draw
    return img


def get_random_square():
    center = (
        random.randrange(
            default_side/2., dims[0] - default_side/2.
        ),
        random.randrange(
            default_side/2., dims[1] - default_side/2.
        )
    )
    return get_square(center, default_side, default_color)


# center is (x, y), side is side length in px
def get_square(center, side, color):
    top_left = tuple(np.add(center, (-side/2., -side/2.)))
    top_right = tuple(np.add(center, (side/2., -side/2.)))
    bot_right = tuple(np.add(center, (side/2., side/2.)))
    bot_left = tuple(np.add(center, (-side/2., side/2.)))
    return {
        'points': [
            top_left,
            top_right,
            bot_right,
            bot_left
        ],
        'color': color
    }


# G
def get_next(x):
    step = 80
    shift = (
        random.randrange(-step, step),
        random.randrange(-step, step)
    )

    x_left_shift = x['points'][0][0] + shift[0]
    x_right_shift = x['points'][2][0] + shift[0]
    y_top_shift = x['points'][0][1] + shift[1]
    y_bot_shift = x['points'][2][1] + shift[1]

    if x_left_shift < 0 or x_right_shift > dims[0]:
        shift = (0, shift[1])
    if y_top_shift < 0 or y_bot_shift > dims[1]:
        shift = (shift[0], 0)

    return {
        'points': [
            tuple(np.add(x['points'][0], shift)),
            tuple(np.add(x['points'][1], shift)),
            tuple(np.add(x['points'][2], shift)),
            tuple(np.add(x['points'][3], shift)),
        ],
        'color': x['color']
    }


def get_likelihood_func(answer):
    answer_img = get_image(answer)
    blurred_a = answer_img.filter(
        ImageFilter.GaussianBlur(radius=blur_radius)
    )
    blurred_data_a = np.array(blurred_a.getdata())[:, 0]
    data_a = np.array(answer_img.getdata())[:, 0]

    def get_likelihood(x):
        b = get_image(x)
        blurred_b = b.filter(
            ImageFilter.GaussianBlur(radius=blur_radius)
        )
        blurred_data_b = np.array(blurred_b.getdata())[:, 0]
        data_b = np.array(b.getdata())[:, 0]

        blurred_diff = np.subtract(blurred_data_a, blurred_data_b)
        diff = np.subtract(data_a, data_b)
        return 1./(np.linalg.norm(blurred_diff) + np.linalg.norm(diff))

    return get_likelihood


def get_prior_prob(x):
    return 1.

default_side = 50
default_color = (0, 0, 0)

blur_radius = 20
twitch_param = 80
num_trials = 50

dims = (400, 300)
root = Tk()
root.geometry(str(dims[0]) + 'x' + str(dims[1]))

center_ans = (100, 150)
correct = get_square(center_ans, default_side, default_color)
metropolis = MH(
    get_next,
    get_likelihood_func,
    get_prior_prob,
    lambda x: render(get_image(x))
)
first_guess = get_random_square()
guess = metropolis.optimize(correct, first_guess, 100)
print 'Answer: ', correct
print 'Guess: ', guess
