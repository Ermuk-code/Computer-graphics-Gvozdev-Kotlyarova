import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

width, height = 400, 400
num_polygons = 8

class Polygon:
    def __init__(self, vertices, color):
        self.vertices = np.array(vertices)
        self.color = color

    def get_points(self):
        return self.vertices[:, :2]

def generate_polygons(n):
    polygons = []
    for _ in range(n):
        num_vertices = np.random.randint(3, 8)
        angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False) + np.random.rand() * (np.pi / num_vertices)
        radius = np.random.uniform(1.0, 3.0)
        vertices = np.column_stack((radius * np.cos(angles), radius * np.sin(angles))) + np.random.rand(2) * 5
        color = np.random.rand(3)
        polygons.append(Polygon(vertices, color))
    return polygons

def draw_axes_and_grid(ax):
    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.set_xticks(np.arange(-10, 11, 1))
    ax.set_yticks(np.arange(-10, 11, 1))
    ax.grid(which='both', linestyle='--', linewidth=0.5)

def warnock_algorithm(polygons, ax):
    for polygon in polygons:
        points = polygon.get_points()
        ax.fill(*zip(*points[:, :2]), color=polygon.color)

def update_scale(val):
    scale = scale_slider.val
    ax.set_xlim([-scale, scale])
    ax.set_ylim([-scale, scale])
    fig.canvas.draw_idle()

fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)

polygons = generate_polygons(num_polygons)

draw_axes_and_grid(ax)
warnock_algorithm(polygons, ax)

ax_scale = plt.axes([0.25, 0.1, 0.65, 0.03])
scale_slider = Slider(ax_scale, 'Scale', 1.0, 20.0, valinit=10)
scale_slider.on_changed(update_scale)

plt.title("Алгоритм Варнока с масштабированием и случайными многоугольниками")
plt.show()
