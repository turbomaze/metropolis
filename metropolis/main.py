from Tkinter import Tk
from metropolis import CubeProblem
from mh import MH

if __name__ == '__main__':
    # gui
    dims = (400, 300)
    root = Tk()
    root.geometry(str(dims[0]) + 'x' + str(dims[1]))

    # domain specific
    problem = CubeProblem(
        root, dims, max_loc=20, radius=20
    )
    correct = (5., 2.)
    metropolis = MH(
        problem.get_next,
        problem.get_likelihood_func,
        problem.get_prior_prob,
        lambda x: problem.render(problem.get_image(x))
    )

    # execution
    first_guess = problem.get_random_cube()
    guess = metropolis.optimize(correct, first_guess, trials=100)
    print 'Answer: ', correct
    print 'Guess: ', guess
