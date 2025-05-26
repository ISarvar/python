import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === Constants ===
G = 6.67430e-11      # Gravitational constant (m^3 kg^-1 s^-2)
DT = 3600 * 24       # Time step: 1 day in seconds

# === Particle class representing celestial bodies ===
class Particle:
    def __init__(self, mass, x, y, vx, vy, name="Particle", color="blue"):
        self.mass = float(mass)
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([vx, vy], dtype=float)
        self.name = name
        self.color = color
        self.path = [self.pos.copy()]
        self.acc = np.zeros(2, dtype=float)

    def update_force(self, force):
        self.acc = force / self.mass

    def update_velocity(self, dt):
        self.vel += self.acc * dt

    def update_position(self, dt):
        self.pos += self.vel * dt
        self.path.append(self.pos.copy())

# === Compute gravitational force between two particles ===
def calculate_gravitational_force(p1, p2):
    r_vec = p2.pos - p1.pos
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.zeros(2)
    r_hat = r_vec / r_mag
    softening = 1e9  # Softening factor to prevent singularities
    force_mag = (G * p1.mass * p2.mass) / (r_mag**2 + softening**2)
    return force_mag * r_hat

# === Create celestial bodies ===
sun     = Particle(1.989e30,   0,         0,       0,     0,     "Sun",     "yellow")
earth   = Particle(5.972e24,   1.496e11,  0,       0,     29780, "Earth",   "blue")
mars    = Particle(0.64171e24, 2.279e11,  0,       0,     24070, "Mars",    "red")
venus   = Particle(4.867e24,   1.082e11,  0,       0,     35020, "Venus",   "orange")
mercury = Particle(0.330e24,   0.579e11,  0,       0,     47360, "Mercury", "gray")

particles = [sun, earth, mars, venus, mercury]

# === Visualization setup ===
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlabel("X position (m)")
ax.set_ylabel("Y position (m)")
ax.set_title("Gravity Simulation: Solar System")

# Set limits based on initial distance (excluding the Sun)
max_dist = max(np.linalg.norm(p.pos) for p in particles if p.name != "Sun")
padding = max_dist * 1.6
ax.set_xlim(-padding, padding)
ax.set_ylim(-padding, padding)
ax.grid(True)

# === Initialize plots ===
scatter_plots = [
    ax.plot([], [], 'o', markersize=(10 if p.name == "Sun" else 5), color=p.color, label=p.name)[0]
    for p in particles
]
path_plots = [
    ax.plot([], [], '-', color=p.color, alpha=0.5)[0]
    for p in particles
]
ax.legend()

# === Initialization function for animation ===
def init():
    for sp in scatter_plots:
        sp.set_data([], [])
    for pp in path_plots:
        pp.set_data([], [])
    return scatter_plots + path_plots

# === Animation update function ===
def animate(frame_num):
    # Compute forces on each particle
    forces = {p.name: np.zeros(2) for p in particles}
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i != j:
                forces[p1.name] += calculate_gravitational_force(p1, p2)

    # Update positions and velocities
    for p in particles:
        p.update_force(forces[p.name])
        p.update_velocity(DT)
        p.update_position(DT)

    # Update plot data
    for idx, p in enumerate(particles):
        scatter_plots[idx].set_data([p.pos[0]], [p.pos[1]])  # Wrap in list to avoid error
        path_array = np.array(p.path)
        path_plots[idx].set_data(path_array[:, 0], path_array[:, 1])

    ax.set_title(f"Gravity Simulation: Solar System — Day: {frame_num}")
    return scatter_plots + path_plots

# === Run the animation ===
num_frames = 365 * 2  # Simulate 2 years
ani = animation.FuncAnimation(
    fig, animate, frames=num_frames, init_func=init,
    blit=True, interval=20, repeat=False
)

plt.show()
print("Simulation completed.")

