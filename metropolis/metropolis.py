from Tkinter import *
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageTk

dims = (400, 300)

center_ans = (100, 150)
default_side = 50
default_color = (0, 0, 0)

blur_radius = 20
twitch_param = 80
num_trials = 50

root = Tk()
root.geometry(str(dims[0]) + 'x' + str(dims[1]))


def uncover_structure(img, trials,):
    guess = get_random_square()
    guess_img = get_image(guess)
    f_x = get_similarity(img, guess_img)
    for i in range(trials):
        step = int(twitch_param * min(1, (60. - i)/50.))
        print 'Round ' + str(i), step

        update = twitch(guess, step)
        update_img = get_image(update)
        f_xp = get_similarity(img, update_img)
        if f_xp <= f_x:
            print f_xp
            f_x = f_xp
            guess = update
            render(update_img)
    return (
        (guess['points'][0][0]+guess['points'][1][0])/2.,
        (guess['points'][0][1]+guess['points'][2][1])/2.
    )


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


def twitch(square, step):
    shift = (
        random.randrange(-step, step),
        random.randrange(-step, step)
    )

    x_left_shift = square['points'][0][0] + shift[0]
    x_right_shift = square['points'][2][0] + shift[0]
    y_top_shift = square['points'][0][1] + shift[1]
    y_bot_shift = square['points'][2][1] + shift[1]

    if x_left_shift < 0 or x_right_shift > dims[0]:
        shift = (0, shift[1])
    if y_top_shift < 0 or y_bot_shift > dims[1]:
        shift = (shift[0], 0)

    return {
        'points': [
            tuple(np.add(square['points'][0], shift)),
            tuple(np.add(square['points'][1], shift)),
            tuple(np.add(square['points'][2], shift)),
            tuple(np.add(square['points'][3], shift)),
        ],
        'color': square['color']
    }


def get_similarity(a, b):
    blurred_a = a.filter(
        ImageFilter.GaussianBlur(radius=blur_radius)
    )
    blurred_b = b.filter(
        ImageFilter.GaussianBlur(radius=blur_radius)
    )
    blurred_data_a = np.array(blurred_a.getdata())[:, 0]
    blurred_data_b = np.array(blurred_b.getdata())[:, 0]
    data_a = np.array(a.getdata())[:, 0]
    data_b = np.array(b.getdata())[:, 0]

    blurred_diff = np.subtract(blurred_data_a, blurred_data_b)
    diff = np.subtract(data_a, data_b)
    return np.linalg.norm(blurred_diff) + np.linalg.norm(diff)


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

correct = get_square(center_ans, default_side, default_color)
correct_img = get_image(correct)
guess = uncover_structure(correct_img, num_trials)
print 'Answer: ', center_ans
print 'Guess: ', guess
