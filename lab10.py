import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Скрыть основное окно Tkinter
Tk().withdraw()

# Открытие диалогового окна для выбора файла
image_path = askopenfilename(title="Выберите изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

# Проверка на успешную загрузку изображения
if not image_path:
    print("Ошибка: Не выбрано изображение.")
else:
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка: Не удалось загрузить изображение по пути: {image_path}")
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Функция для отображения изображений
        def show_images(images, titles):
            plt.figure(figsize=(15, 5))
            for i in range(len(images)):
                plt.subplot(1, len(images), i + 1)
                plt.imshow(images[i])
                plt.title(titles[i])
                plt.axis('off')
            plt.show()

        # Параметры преобразований
        scale_factor = 2.0
        angle = 230
        shear_factor = 0.5

        # Масштабирование
        scaled_image_nearest = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)
        scaled_image_bilinear = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
        scaled_image_bicubic = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        # Поворот
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image_nearest = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_NEAREST)
        rotated_image_bilinear = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR)
        rotated_image_bicubic = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC)

        # Скошение
        new_width = int(w + h * shear_factor)
        shear_matrix = np.float32([[1, shear_factor, 0], [0, 1, 0]])
        sheared_image_nearest = cv2.warpAffine(image, shear_matrix, (new_width, h), flags=cv2.INTER_NEAREST)
        sheared_image_bilinear = cv2.warpAffine(image, shear_matrix, (new_width, h), flags=cv2.INTER_LINEAR)
        sheared_image_bicubic = cv2.warpAffine(image, shear_matrix, (new_width, h), flags=cv2.INTER_CUBIC)

        # Отображение результатов
        show_images([scaled_image_nearest, scaled_image_bilinear, scaled_image_bicubic],
                    ['Масштабирование - По ближайшему соседу', 'Масштабирование - Билинейный', 'Масштабирование - Бикубический'])

        show_images([rotated_image_nearest, rotated_image_bilinear, rotated_image_bicubic],
                    ['Поворот - По ближайшему соседу', 'Поворот - Билинейный', 'Поворот - Бикубический'])

        show_images([sheared_image_nearest, sheared_image_bilinear, sheared_image_bicubic],
                    ['Скос - По ближайшему соседу', 'Скос - Билинейный', 'Скос - Бикубический'])
