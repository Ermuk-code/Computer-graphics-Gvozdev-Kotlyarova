import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
5

def du_sabin_surface(vertices, resolution=100):
    # Генерация сетки значений x и y
    x = np.linspace(-5, 5, resolution)
    y = np.linspace(-5, 5, resolution)
    X, Y = np.meshgrid(x, y)

    Z = np.zeros_like(X)

    for i, vertex in enumerate(vertices):
        z_value = vertex[2]  # z-координата вершины
        Z += z_value * np.exp(-((X - vertex[0]) ** 2 + (Y - vertex[1]) ** 2))

        print(f'Этап {i + 1}: Добавлена вершина {vertex} (z = {z_value})')

    return X, Y, Z

num_vertices = int(input("Введите количество вершин: "))

vertices = []
for i in range(num_vertices):
    x = np.random.uniform(-5, 5)  # Случайное значение x в диапазоне [-5, 5]
    y = np.random.uniform(-5, 5)  # Случайное значение y в диапазоне [-5, 5]
    z = np.random.uniform(0, 2)  # Случайное значение z в диапазоне [0, 2]
    vertices.append((x, y, z))

X, Y, Z = du_sabin_surface(vertices)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_title('Финальная поверхность Ду-Сабина')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()
