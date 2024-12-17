import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def cohen_sutherland_clip(p1, p2, x_min, y_min, x_max, y_max):
    def compute_code(x, y):
        code = 0
        if x < x_min:
            code |= 1  
        elif x > x_max:
            code |= 2  
        if y < y_min:
            code |= 4  
        elif y > y_max:
            code |= 8  
        return code

    code1 = compute_code(p1[0], p1[1])
    code2 = compute_code(p2[0], p2[1])
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            code_out = code1 if code1 else code2
            if code_out & 8:  
                x = p1[0] + (p2[0] - p1[0]) * (y_max - p1[1]) / (p2[1] - p1[1])
                y = y_max
            elif code_out & 4:  
                x = p1[0] + (p2[0] - p1[0]) * (y_min - p1[1]) / (p2[1] - p1[1])
                y = y_min
            elif code_out & 2:  
                y = p1[1] + (p2[1] - p1[1]) * (x_max - p1[0]) / (p2[0] - p1[0])
                x = x_max
            elif code_out & 1:  
                y = p1[1] + (p2[1] - p1[1]) * (x_min - p1[0]) / (p2[0] - p1[0])
                x = x_min

            if code_out == code1:
                p1 = [x, y]
                code1 = compute_code(p1[0], p1[1])
            else:
                p2 = [x, y]
                code2 = compute_code(p2[0], p2[1])

    return (accept, p1, p2)


def input_segments():
    segments = []
    n = int(input("Введите количество отрезков: "))
    for i in range(n):
        x1 = float(input(f"Введите x1 для отрезка {i + 1}: "))
        y1 = float(input(f"Введите y1 для отрезка {i + 1}: "))
        x2 = float(input(f"Введите x2 для отрезка {i + 1}: "))
        y2 = float(input(f"Введите y2 для отрезка {i + 1}: "))
        segments.append(((x1, y1), (x2, y2)))

    x_min, y_min, x_max, y_max = map(float, input("Введите значение для окна (x_min, y_min, x_max, y_max): ").split())

    return segments, x_min, y_min, x_max, y_max


def show_segments(segments, x_min, y_min, x_max, y_max):
    plt.figure()
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)
    plt.plot([x_min, x_min, x_max, x_max, x_min],
             [y_min, y_max, y_max, y_min, y_min], 'r-')

    for segment in segments:
        p1, p2 = segment
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Исходные отрезки")
    plt.grid()
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.show()


def show_clipped(segments, x_min, y_min, x_max, y_max):
    plt.figure()
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)
    plt.plot([x_min, x_min, x_max, x_max, x_min],
             [y_min, y_max, y_max, y_min, y_min], 'r-')

    for segment in segments:
        p1, p2 = segment
        accept, new_p1, new_p2 = cohen_sutherland_clip(p1, p2, x_min, y_min, x_max, y_max)

        if accept:
            plt.plot([new_p1[0], new_p2[0]], [new_p1[1], new_p2[1]], 'b-')
        else:
            if new_p1 and new_p2:
                plt.plot([new_p1[0], new_p2[0]], [new_p1[1], new_p2[1]], 'g--')  # Отрисовка отсеченной части

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Отсеченные отрезки")
    plt.grid()
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.show()


def main():
    segments, x_min, y_min, x_max, y_max = input_segments()

    root = tk.Tk()
    root.title("Cohen-Sutherland Clipping")

    frame = tk.Frame(root)
    frame.pack()

    button_show_segments = tk.Button(frame, text="Показать исходные отрезки",
                                     command=lambda: show_segments(segments, x_min, y_min, x_max, y_max))
    button_show_segments.pack(side=tk.LEFT)

    button_show_clipped = tk.Button(frame, text="Показать отсеченные отрезки",
                                    command=lambda: show_clipped(segments, x_min, y_min, x_max, y_max))
    button_show_clipped.pack(side=tk.LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
