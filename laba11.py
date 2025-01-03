from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QLabel, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt


class CurveApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Построение кривых и поверхностей")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.iterations_input = QLineEdit(self)
        self.iterations_input.setPlaceholderText("Количество итераций/точек")
        self.layout.addWidget(QLabel("Введите параметр:"))
        self.layout.addWidget(self.iterations_input)

        self.bezier_button = QPushButton("Квадратичная кривая Безье", self)
        self.bezier_button.clicked.connect(self.plot_bezier)
        self.layout.addWidget(self.bezier_button)

        self.chaikin_button = QPushButton("Кривая Чайкина", self)
        self.chaikin_button.clicked.connect(self.plot_chaikin)
        self.layout.addWidget(self.chaikin_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def plot_bezier(self):
        try:
            num_points = int(self.iterations_input.text())
            if num_points < 3:
                raise ValueError("Для кривой Безье нужно не менее 3 точек.")
            t_values = np.linspace(0, 1, 100)
            control_points = np.random.rand(num_points, 2) * 10
            curve_points = self.quadratic_bezier(control_points[:3], t_values)

            self.ax.clear()
            self.ax.plot(control_points[:, 0], control_points[:, 1], 'ro-', label="Контрольные точки")
            self.ax.plot(curve_points[:, 0], curve_points[:, 1], 'b-', label="Кривая Безье")
            self.ax.legend()
            self.canvas.draw()
        except ValueError as e:
            print(f"Ошибка: {e}")

    def quadratic_bezier(self, control_points, t_values):
        curve_points = []
        for t in t_values:
            p_t = (1 - t) ** 2 * control_points[0] + 2 * (1 - t) * t * control_points[1] + t ** 2 * control_points[2]
            curve_points.append(p_t)
        return np.array(curve_points)

    def plot_chaikin(self):
        try:
            iterations = int(self.iterations_input.text())
            if iterations < 1:
                raise ValueError("Итерации должны быть больше 0.")

            num_points = int(self.iterations_input.text())
            control_points = np.random.rand(num_points, 2) * 10

            refined_points = self.chaikin_curve(control_points, iterations)

            self.ax.clear()
            self.ax.plot(control_points[:, 0], control_points[:, 1], 'ro-', label="Контрольные точки")
            self.ax.plot(refined_points[:, 0], refined_points[:, 1], 'g-', label="Кривая Чайкина")
            self.ax.legend()
            self.canvas.draw()
        except ValueError as e:
            print(f"Ошибка: {e}")

    def chaikin_curve(self, control_points, iterations):
        for _ in range(iterations):
            new_points = []
            for i in range(len(control_points) - 1):
                q = 0.75 * control_points[i] + 0.25 * control_points[i + 1]
                r = 0.25 * control_points[i] + 0.75 * control_points[i + 1]
                new_points.extend([q, r])
            control_points = np.array(new_points)
        return control_points


app = QApplication([])
window = CurveApp()
window.show()
app.exec_()
