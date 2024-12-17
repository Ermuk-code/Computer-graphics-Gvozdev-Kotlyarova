from PIL import Image, ImageDraw, ImageTk
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog, messagebox


class ImageTransformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение")

        self.image = None
        self.transformed_image = None
        self.image_frame = tk.Label(root, text="Исходное изоражение")
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        self.transformed_frame = tk.Label(root, text="Обработанное изображение")
        self.transformed_frame.grid(row=0, column=1, padx=10, pady=10)

        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.grid(row=1, column=0, pady=10)
        self.width_label = tk.Label(root, text="Ширина нового изображения:")
        self.width_label.grid(row=2, column=0, pady=5)

        self.width_entry = tk.Entry(root)
        self.width_entry.grid(row=2, column=1, pady=5)

        self.height_label = tk.Label(root, text="Высота нового изображения:")
        self.height_label.grid(row=3, column=0, pady=5)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=3, column=1, pady=5)
        self.accept_button = tk.Button(root, text="Принять координаты", command=self.accept_dimensions)
        self.accept_button.grid(row=4, column=0, pady=10)
        self.create_button = tk.Button(root, text="Создать новое изображение", command=self.create_new_image)
        self.create_button.grid(row=4, column=1, pady=5)

        self.axes_button = tk.Button(root, text="Добавить оси", command=self.draw_axes_and_function)
        self.axes_button.grid(row=5, column=0, pady=5)

        self.transform_button = tk.Button(root, text="Преобразование по варианту", command=self.add_fragment)
        self.transform_button.grid(row=6, column=0, pady=5)

        self.save_button = tk.Button(root, text="Сохранить изображение", command=self.save_result)
        self.save_button.grid(row=6, column=1, pady=10)

        self.new_image_width = None
        self.new_image_height = None

    def create_new_image(self):
        self.transformed_image = Image.new('RGB', (self.new_image_width, self.new_image_height), (255, 255, 255))
        self.display_image(self.transformed_image, self.transformed_frame)

    def accept_dimensions(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.new_image_width = width
            self.new_image_height = height
            messagebox.showinfo("Данные введены", f"Ширина: {width}, Высота: {height}")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Выберите изображение")
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image, self.image_frame)

    def add_fragment(self):
        if self.image:
            original_pixels = self.image.load()
            new_pixels = self.transformed_image.load()
            fragment_size = 100

            # Вырезаем фрагмент из центра левого нижнего угла
            left_x = 0
            bottom_y = self.image.height
            # Определяем верхнюю границу фрагмента с учетом высоты фрагмента
            top_left_y = bottom_y - fragment_size

            for y in range(fragment_size):
                for x in range(fragment_size):
                    original_x = left_x + x
                    original_y = top_left_y + y

                    if 0 <= original_x < self.image.width and 0 <= original_y < self.image.height:
                        # Обновите координаты для размещения в верном месте
                        new_x = self.transformed_image.width - fragment_size + x
                        new_y = self.transformed_image.height - fragment_size + y  # Смещаем y на размер фрагмента

                        if 0 <= new_x < self.transformed_image.width and 0 <= new_y < self.transformed_image.height:
                            new_pixels[new_x, new_y] = original_pixels[original_x, original_y]

            self.display_image(self.transformed_image, self.transformed_frame)

    def draw_axes_and_function(self):
        draw = ImageDraw.Draw(self.transformed_image)
        width, height = self.transformed_image.size

        mid_x = width // 2
        mid_y = height // 2
        draw.line((0, mid_y, width, mid_y), fill='black', width=2)
        draw.line((mid_x, 0, mid_x, height), fill='black', width=2)

        scale = 50
        for x in range(-mid_x, mid_x):
            y = int(scale * (x / scale) * math.sin(x / scale))
            draw.point((mid_x + x, mid_y - y), fill='blue')
        self.display_image(self.transformed_image, self.transformed_frame)

    def display_image(self, image, frame):
        image_copy = image.copy()
        image_copy.thumbnail((300, 300))
        image_copy.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(image_copy)
        frame.config(image=img_tk)
        frame.image = img_tk

    def save_result(self):
        if self.transformed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.transformed_image.save(file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTransformApp(root)
    root.mainloop()
