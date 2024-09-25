from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def plot_circle_to_bmp(x_center, y_center, radius, filename="circle.bmp"):
    img_size = (300, 300)

    img = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(img)

    x = 0
    y = radius
    d = 3 - 2 * radius

    def draw_circle(draw, x_center, y_center, x, y):
        draw.point((x_center + x, y_center + y), fill="black")
        draw.point((x_center - x, y_center + y), fill="black")
        draw.point((x_center + x, y_center - y), fill="black")
        draw.point((x_center - x, y_center - y), fill="black")
        draw.point((x_center + y, y_center + x), fill="black")
        draw.point((x_center - y, y_center + x), fill="black")
        draw.point((x_center + y, y_center - x), fill="black")
        draw.point((x_center - y, y_center - x), fill="black")

    while y >= x:
        draw_circle(draw, x_center, y_center, x, y)
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

    img.save("circle.bmp")
    print(f"Окружность сохранена как circle.bmp")

if __name__ == "__main__":
    x_center = int(input("Введите координату X центра окружности: "))
    y_center = int(input("Введите координату Y центра окружности: "))
    radius = int(input("Введите радиус окружности: "))

    plot_circle_to_bmp(x_center, y_center, radius)
