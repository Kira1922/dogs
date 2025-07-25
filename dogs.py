import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


def show_image():
    image_url = get_random_dog_image()
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            label.config(image=img)
            label.image = img

        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")


window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")

label = Label()
label.pack(padx=10, pady=10)

button = Button(text="Загрузить изображение", command=show_image)
button.pack(padx=10, pady=10)

window.mainloop()
