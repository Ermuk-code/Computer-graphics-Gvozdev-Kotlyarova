import cv2
import numpy as np
from tkinter import Tk, Button, Label, Canvas, filedialog
from PIL import Image, ImageTk

def apply_low_pass_filter(image):
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32) / 9
    return cv2.filter2D(image, -1, kernel)

def apply_high_pass_filter(image, kernel):
    return cv2.filter2D(image, -1, kernel)

def process_image_variant6():
    global processed_image, original_image
    if original_image is None:
        result_label.config(text="Сначала откройте изображение!")
        return
    height, width, _ = original_image.shape
    left_part = original_image[:, :width // 2]
    right_part = original_image[:, width // 2:]
    low_pass_left = apply_low_pass_filter(left_part)
    processed_left = cv2.subtract(left_part, low_pass_left)
    laplacian_kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float32)
    gaussian_kernel = cv2.getGaussianKernel(ksize=5, sigma=1)
    laplacian_gaussian_kernel = np.outer(gaussian_kernel, gaussian_kernel.T)
    high_pass_right_gaussian = apply_high_pass_filter(right_part, laplacian_gaussian_kernel)
    processed_image = np.hstack((processed_left, high_pass_right_gaussian))
    display_image(processed_image, result_canvas, max_width=500, max_height=300)
    result_label.config(text="Обработка завершена!")

def open_image():
    global original_image

    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.bmp;*.tiff")])
    if not file_path:
        return

    try:
        original_image = cv2.imread(file_path)
        if original_image is None:
            raise ValueError("Ошибка загрузки изображения. Формат может быть неподдерживаемым.")

        display_image(original_image, original_canvas, max_width=500, max_height=300)
        result_label.config(text="Изображение успешно загружено!")
    except Exception as e:
        result_label.config(text=f"Ошибка: {e}")

def save_image():
    global processed_image

    if processed_image is None:
        result_label.config(text="Сначала обработайте изображение!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("BMP Image", "*.bmp")])
    if not file_path:
        return

    try:
        cv2.imwrite(file_path, processed_image)
        result_label.config(text=f"Результат сохранен: {file_path}")
    except Exception as e:
        result_label.config(text=f"Ошибка сохранения: {e}")

def display_image(image, canvas, max_width, max_height):
    height, width, _ = image.shape
    scale = min(max_width / width, max_height / height, 1.0)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = cv2.resize(image, (new_width, new_height))
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    canvas.delete("all")
    canvas.image = image_tk
    canvas.config(width=new_width, height=new_height)
    canvas.create_image(0, 0, anchor="nw", image=image_tk)

root = Tk()
root.title("Фильтрация изображения - Вариант 6")
original_image = None
processed_image = None
open_button = Button(root, text="Открыть изображение", command=open_image)
open_button.pack()
process_button = Button(root, text="Обработать изображение", command=process_image_variant6)
process_button.pack()
save_button = Button(root, text="Сохранить результат", command=save_image)
save_button.pack()
original_label = Label(root, text="Исходное изображение:")
original_label.pack()
original_canvas = Canvas(root, width=500, height=300, bg="gray")
original_canvas.pack()
result_label = Label(root, text="Результат:")
result_label.pack()
result_canvas = Canvas(root, width=500, height=300, bg="gray")
result_canvas.pack()
root.mainloop()
