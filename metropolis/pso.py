import random
import time


class Particle(object):
    def __init__(self, pos, score, vel):
        self.pos = list(pos)
        self.best = score
        self.best_pos = list(pos)
        self.vel = vel


class PSO(object):
    # @param params   - list of [min, max] pairs, one per param
    # @param pi_maker - the posterior likelihood function maker
    def __init__(self, params, pi_maker):
        self._w = 0.5729
        self._p = 0.15
        self._g = 0.13
        self._r = 0.085
        self._iv = 0.5

        self.d = len(params)
        self.params = params
        self.pi_maker = pi_maker


    def get_rand_pos(self):
        return [
            random.random() for _ in range(self.d)
        ]

    def pos_to_params(self, pos):
        return [
            self.params[i][0] + pos[i] * (
                self.params[i][1] - self.params[i][0]
            ) for i in range(self.d)
        ]

    def optimize(self, n, t, goal, each_time):
        start = time.clock()
        pi = self.pi_maker(goal)

        # init
        particles = []
        best = float('-inf')
        best_pos = []
        for i in range(n):
            pos = self.get_rand_pos()
            score = pi(self.pos_to_params(pos))
            vel = [
                2*self._iv*random.random() - self._iv
                for i in range(self.d)
            ]
            particles.append(Particle(pos, score, vel))

            if score > best:
                best = score
                best_pos = list(pos)

        # iterate
        for _ in range(t):
            if _ % 10 == 0:
                print best, self.pos_to_params(best_pos)
            for i in range(n):
                p = particles[i]

                # velocity update
                rp = random.random()
                rg = random.random()
                for j in range(self.d):
                    pdiff = p.best_pos[j] - p.pos[j]
                    gdiff = best_pos[j] - p.pos[j]
                    p.vel[j] = self._w * p.vel[j]
                    p.vel[j] += self._p * rp * pdiff
                    p.vel[j] += self._g * rg * gdiff
                    p.vel[j] += 2 * self._r * random.random() - self._r

                # position update
                for j in range(self.d):
                    p.pos[j] = p.pos[j] + p.vel[j]
                    p.pos[j] = max(0, min(1, p.pos[j]))

                # update the best score
                new_score = pi(self.pos_to_params(p.pos))
                if new_score > p.best:
                    p.best = new_score
                    p.best_pos = list(p.pos)

                if new_score > best:
                    best = new_score
                    best_pos = list(p.pos)

            each_time(particles)

        # logging
        duration = time.clock() - start
        print str(t) + ' steps in ' + str(duration) + 's'

        return self.pos_to_params(best_pos)


