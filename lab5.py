import numpy as np
import matplotlib.pyplot as plt

def draw_triangle(ax, v1, v2, v3):
    triangle = np.array([v1, v2, v3, v1])
    ax.fill(triangle[:, 0], triangle[:, 1], edgecolor='black', alpha=0.3)

num_sides = 6
angle = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
angle += np.pi / 2
hexagon = np.array([[np.cos(a), np.sin(a)] for a in angle])

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(*np.append(hexagon, [hexagon[0]], axis=0).T, color='black')

A, B, C, D, E, F = hexagon
ax.plot([B[0], F[0]], [B[1], F[1]], color='black')  
ax.plot([C[0], E[0]], [C[1], E[1]], color='black')  

O = (B + F) / 2
ax.plot(*O, 'o', color='black')  
ax.plot([A[0], O[0]], [A[1], O[1]], color='black')  

G = B + (O - B) / 3
I = F - (F - O) / 3

ax.plot([A[0], G[0]], [A[1], G[1]], 'k--')  
ax.plot([A[0], I[0]], [A[1], I[1]], 'k--')  

H = (C + E) / 2
ax.plot(*H, 'o', color='black')  
ax.plot([H[0], D[0]], [H[1], D[1]], 'k--')  

Y = C + (H - C) / 3
X = E - (E - H) / 3

ax.plot([X[0], D[0]], [X[1], D[1]], color='black')  
ax.plot([Y[0], D[0]], [Y[1], D[1]], color='black')  
ax.plot([O[0], X[0]], [O[1], X[1]], color='black')  
ax.plot([O[0], Y[0]], [O[1], Y[1]], color='black')  
ax.plot([B[0], Y[0]], [B[1], Y[1]], color='black')  
ax.plot([X[0], F[0]], [X[1], F[1]], color='black')  

ax.plot([H[0], G[0]], [H[1], G[1]], 'k--')  
ax.plot([H[0], I[0]], [H[1], I[1]], 'k--')  
ax.plot([I[0], E[0]], [I[1], E[1]], 'k--')  
ax.plot([G[0], C[0]], [G[1], C[1]], 'k--')  

ax.set_aspect('equal')
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])
plt.title('Hexagon with Connections')
plt.grid()
plt.show()
