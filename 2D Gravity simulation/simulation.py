import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider

# === Constants ===
G = 6.67430e-11      # Gravitational constant (m^3 kg^-1 s^-2)
DT = 3600 * 24       # Base time step: 1 day in seconds

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

def calculate_gravitational_force(p1, p2):
    r_vec = p2.pos - p1.pos
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.zeros(2)
    r_hat = r_vec / r_mag
    softening = 1e9
    force_mag = (G * p1.mass * p2.mass) / (r_mag**2 + softening**2)
    return force_mag * r_hat

# === Create celestial bodies ===
sun     = Particle(1.989e30,   0,         0,       0,     0,     "Sun",     "yellow")
earth   = Particle(5.972e24,   1.496e11,  0,       0,     29780, "Earth",   "blue")
mars    = Particle(0.64171e24, 2.279e11,  0,       0,     24070, "Mars",    "red")
venus   = Particle(4.867e24,   1.082e11,  0,       0,     35020, "Venus",   "orange")
mercury = Particle(0.330e24,   0.579e11,  0,       0,     47360, "Mercury", "gray")
jupiter = Particle(1.898e27,   7.785e11,  0,       0,     13070, "Jupiter", "orange")
saturn  = Particle(568e24,     1.433e12,  0,       0,     9690,  "Saturn",  "gold")
uranus  = Particle(86.8e24,    2.877e12,  0,       0,     6810,  "Uranus",  "lightblue")
neptune = Particle(102e24,     4.503e12,  0,       0,     5430,  "Neptune", "darkblue")

particles = [sun, earth, mars, venus, mercury, jupiter, saturn, uranus, neptune]

# === Visualization setup ===
plt.ion()
fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_aspect('equal')
ax.set_xlabel("X (m)", color='white')
ax.set_ylabel("Y (m)", color='white')
ax.set_title("🌌 Solar System Simulation", color='white', fontsize=16)

max_dist = max(np.linalg.norm(p.pos) for p in particles if p.name != "Sun")
padding = max_dist * 1.6
ax.set_xlim(-padding, padding)
ax.set_ylim(-padding, padding)
ax.tick_params(colors='white')
ax.grid(True, color='gray', alpha=0.3)

scatter_plots = [
    ax.plot([], [], 'o', markersize=(10 if p.name == "Sun" else 5), color=p.color, label=p.name)[0]
    for p in particles
]
path_plots = [
    ax.plot([], [], '-', color=p.color, alpha=0.5)[0]
    for p in particles
]
legend = ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
for text in legend.get_texts():
    text.set_color("white")

# === Animation state ===
running = True
speed_multiplier = 1.0

# === Init function ===
def init():
    for sp in scatter_plots:
        sp.set_data([], [])
    for pp in path_plots:
        pp.set_data([], [])
    return scatter_plots + path_plots

# === Animation update ===
def animate(frame_num):
    if not running:
        return scatter_plots + path_plots

    dt = DT * speed_multiplier
    forces = {p.name: np.zeros(2) for p in particles}
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i != j:
                forces[p1.name] += calculate_gravitational_force(p1, p2)

    for p in particles:
        p.update_force(forces[p.name])
        p.update_velocity(dt)
        p.update_position(dt)

    for idx, p in enumerate(particles):
        scatter_plots[idx].set_data([p.pos[0]], [p.pos[1]])
        path_array = np.array(p.path)
        path_plots[idx].set_data(path_array[:, 0], path_array[:, 1])

    ax.set_title(f"🌌 Solar System Simulation — Day: {frame_num}", color='white')
    return scatter_plots + path_plots

ani = animation.FuncAnimation(
    fig, animate, init_func=init,
    blit=True, interval=20, repeat=True, cache_frame_data=False
)

# === Controls ===
ax_zoom_in = plt.axes([0.52, 0.03, 0.06, 0.04])
ax_zoom_out = plt.axes([0.59, 0.03, 0.06, 0.04])

ax.set_title("Solar System Simulation", color='white', fontsize=16)
btn_zoom_in = Button(ax_zoom_in, '+', color='gray', hovercolor='lightgreen')
btn_zoom_out = Button(ax_zoom_out, '-', color='gray', hovercolor='lightcoral')

def toggle_play(event):
    global running
    running = not running

def zoom(factor):
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    x_center = (cur_xlim[0] + cur_xlim[1]) / 2
    y_center = (cur_ylim[0] + cur_ylim[1]) / 2
    width = (cur_xlim[1] - cur_xlim[0]) * factor
    height = (cur_ylim[1] - cur_ylim[0]) * factor
    ax.set_xlim([x_center - width/2, x_center + width/2])
    ax.set_ylim([y_center - height/2, y_center + height/2])
    fig.canvas.draw_idle()

def zoom_in(event):
    zoom(1 / 1.2)

def zoom_out(event):
    zoom(1.2)

btn_zoom_in.on_clicked(zoom_in)
btn_zoom_out.on_clicked(zoom_out)

plt.show(block=True)
print("Simulation completed.")