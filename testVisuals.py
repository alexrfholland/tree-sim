import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')

class ChargedParticle:
    def __init__(self, pos, charge):
        self.pos = np.asarray(pos)
        self.charge = charge
        
    def compute_field(self, x, y):
        X, Y = np.meshgrid(x, y)
        u_i = np.hstack((X.ravel()[:, np.newaxis],  Y.ravel()[:, np.newaxis])) - self.pos
        r = np.sqrt((X - self.pos[0])**2 + (Y - self.pos[1])**2)
        field = ((self.charge / r**2).ravel()[:, np.newaxis] * u_i).reshape(X.shape + (2,))
        return field
    
    def compute_potential(self, x, y):
        X, Y = np.meshgrid(x, y)
        r = np.sqrt((X - self.pos[0])**2 + (Y - self.pos[1])**2)
        potential = self.charge / r
        return potential

x = np.linspace(-5, 5, 100)
y = np.linspace(-4, 4, 80)

Y, X = np.meshgrid(x, y)

q1 = ChargedParticle((-1, 0), -1)
q2 = ChargedParticle((1, 0), 1)

field1 = q1.compute_field(x, y)
field2 = q2.compute_field(x, y)

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 10))
ax1.streamplot(x, y, u=field1[:, :, 0], v=field1[:, :, 1])
ax1.set_title("particle with negative charge");
ax1.axis('equal')
ax2.streamplot(x, y, u=field2[:, :, 0], v=field2[:, :, 1])
ax2.set_title("particle with positive charge");
ax2.axis('equal');

pot1 = q1.compute_potential(x, y)
pot2 = q2.compute_potential(x, y)

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(6, 10))
map1 = ax1.pcolormesh(x, y, pot1, vmin=-10, vmax=10)
ax1.set_title("particle with negative charge");
ax1.axis('equal')
plt.colorbar(map1, ax=ax1)
map2 = ax2.pcolormesh(x, y, pot2, vmin=-10, vmax=10)
ax2.set_title("particle with positive charge");
ax2.axis('equal');
plt.colorbar(map2, ax=ax2);

plt.show()
