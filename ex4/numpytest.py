import numpy as np
import copy
import particle
import time

def residual_resample(weights):
    N = len(weights)
    indexes = np.zeros(N, 'i')

    # take int(N*w) copies of each weight, which ensures particles with the
    # same weight are drawn uniformly
    num_copies = (np.floor(N*np.asarray(weights))).astype(int)
    k = 0
    for i in range(N):
        for _ in range(num_copies[i]): # make n copies
            indexes[k] = i
            k += 1

    # use multinormal resample on the residual to fill up the rest. This
    # maximizes the variance of the samples
    residual = weights - num_copies     # get fractional part
    residual /= sum(residual)           # normalize
    cumulative_sum = np.cumsum(residual)
    cumulative_sum[-1] = 1. # avoid round-off errors: ensures sum is exactly one
    indexes[k:N] = np.searchsorted(cumulative_sum, random(N-k))

    return indexes

def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points. 
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)

    return particles

#Time runtime of the particle filter
start_time = time.time()

#

end_time = time.time()
print("Time elapsed for numpy filter: ", end_time - start_time)

#Time runtime of the particle filter
start_time = time.time()
num_particles = 1000
particles = initialize_particles(num_particles)
#print("Time to initialize particles: %s seconds" % (time.time() - start_time))
new_particles = []
for i in range(num_particles):
    r = np.random.ranf()
    sum_of_weights = 0
    for p in particles:
        sum_of_weights += p.getWeight()
        if sum_of_weights >= r:
            new_particles.append(copy.copy(p))
            break
particles = new_particles

end_time = time.time()
print("Time elapsed for normal filter: ", end_time - start_time)