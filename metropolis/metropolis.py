import random
import cv2
import numpy as np
from Tkinter import Label
from utils import draw_from_model
from PIL import Image, ImageDraw, ImageFilter, ImageTk


def get_corners(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    gray = np.float32(gray)
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    return [c[0] for c in np.int0(corners)]


class SquareProblem(object):
    def __init__(self, root, dims, side, color, radius):
        self.root = root
        self.dims = dims
        self.side = side
        self.color = color
        self.radius = radius

    def render(self, img):
        blurred = img.filter(
            ImageFilter.GaussianBlur(radius=self.radius)
        )

        tk_img = ImageTk.PhotoImage(blurred)
        label_image = Label(self.root, image=tk_img)
        label_image.place(
            x=0, y=0,
            width=img.size[0],
            height=img.size[1]
        )
        self.root.update()

    def get_image(self, polygon):
        data = np.zeros(
            (self.dims[1], self.dims[0], 3),
            dtype=np.uint8
        )
        data.fill(255)
        img = Image.fromarray(data, 'RGB')
        draw = ImageDraw.Draw(img, 'RGB')
        draw.polygon(polygon['points'], polygon['color'])
        del draw
        return img

    def get_random_square(self):
        center = (
            random.randrange(
                self.side/2., self.dims[0] - self.side/2.
            ),
            random.randrange(
                self.side/2., self.dims[1] - self.side/2.
            )
        )
        return self.get_square(center, self.side, self.color)

    # center is (x, y), side is side length in px
    def get_square(self, center, side, color):
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
    def get_next(self, x):
        step = 80
        shift = (
            random.randrange(-step, step),
            random.randrange(-step, step)
        )

        x_left_shift = x['points'][0][0] + shift[0]
        x_right_shift = x['points'][2][0] + shift[0]
        y_top_shift = x['points'][0][1] + shift[1]
        y_bot_shift = x['points'][2][1] + shift[1]

        if x_left_shift < 0 or x_right_shift > self.dims[0]:
            shift = (0, shift[1])
        if y_top_shift < 0 or y_bot_shift > self.dims[1]:
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

    def get_likelihood_func(self, answer):
        answer_img = self.get_image(answer)
        blurred_a = answer_img.filter(
            ImageFilter.GaussianBlur(radius=self.radius)
        )
        blurred_data_a = np.array(blurred_a.getdata())[:, 0]
        data_a = np.array(answer_img.getdata())[:, 0]

        def get_likelihood(x):
            b = self.get_image(x)
            blurred_b = b.filter(
                ImageFilter.GaussianBlur(radius=self.radius)
            )
            blurred_data_b = np.array(blurred_b.getdata())[:, 0]
            data_b = np.array(b.getdata())[:, 0]

            blurred_diff = np.subtract(blurred_data_a, blurred_data_b)
            diff = np.subtract(data_a, data_b)
            return 1./(np.linalg.norm(blurred_diff) + np.linalg.norm(diff))

        return get_likelihood

    def get_prior_prob(self, x):
        return 1.


class CubeProblem(object):
    def __init__(self, root, dims, max_loc, radius):
        self.root = root
        self.dims = dims
        self.max_loc = max_loc
        self.radius = radius

    def render(self, img):
        draw = ImageDraw.Draw(img)
        w = 3
        for c in get_corners(img):
            draw.rectangle(
                [c[0]-w, c[1]-w, c[0]+w, c[1]+w],
                fill=(0, 255, 0)
            )
        tk_img = ImageTk.PhotoImage(img)
        label_image = Label(self.root, image=tk_img)
        label_image.place(
            x=0, y=0,
            width=img.size[0],
            height=img.size[1]
        )
        self.root.update()

    def get_image(self, x):
        im = Image.new('RGB', self.dims, '#ffffff')
        draw = ImageDraw.Draw(im)
        camera = np.matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [15, 10, 30]
        ])
        model = [
            [20, (0, 0, 0), '#000000', 1],
            [7, (x[0], 0, x[1]), '#ff0000', 0]
        ]
        draw_from_model(draw, camera, model, fov=200)
        return im

    def get_random_cube(self):
        center = (
            random.uniform(0, self.max_loc),
            random.uniform(0, self.max_loc)
        )
        return center

    # G
    def get_next(self, x, k):
        step = 5.
        shift = random.uniform(-step, step)
        if x[k] + shift < 0 or x[k] + shift > self.max_loc:
            return x
        else:
            x_list = list(x)
            x_list[k] += shift
            return tuple(x_list)

    def get_likelihood_func(self, answer):
        answer_img = self.get_image(answer)
        corners_a = get_corners(answer_img)
        data_a = np.array(answer_img.getdata())[:, 0]

        def get_likelihood(x):
            b = self.get_image(x)
            corners_b = get_corners(b)
            data_b = np.array(b.getdata())[:, 0]

            # direct error
            diff = np.linalg.norm(np.subtract(data_a, data_b))

            # compare corner error
            max_err = self.dims[0]**2 + self.dims[1]**2
            corner_error = max_err * max(
                0, len(corners_a) - len(corners_b)
            )
            for ca in corners_a:
                for cb in corners_b:
                    c_diff = np.subtract(ca, cb)
                    corner_error += np.linalg.norm(c_diff)**2

            return 1./(corner_error**0.5 + diff)

        return get_likelihood

    def get_prior_prob(self, x):
        return 1.
