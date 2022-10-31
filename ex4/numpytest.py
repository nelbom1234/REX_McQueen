import numpy as np
import copy
import particle
import time

def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points. 
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)

    return particles

#Time runtime of the particle filter
start_time = time.time()

num_particles = 1000
particles = initialize_particles(num_particles)
#Resample particles using numpy
particles = np.random.choice(particles, num_particles, p=[p.weight for p in particles])

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