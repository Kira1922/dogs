import requests
from tkinter import Tk, Toplevel, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

def get_random_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Ошибка при запросе к API: {e}")
        return None

def show_image():
    status_label.config(text="Загрузка...")
    image_url = get_random_dog_image()

    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)

            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Пёсик {notebook.index('end') + 1}")
            label = ttk.Label(tab, image=img)
            label.image = img
            label.pack(padx=10, pady=10)

            status_label.config(text="")
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

def start_progress():
    progress['value'] = 0
    progress.start(30)
    window.after(3000, lambda: [progress.stop(), show_image()])

def ochistka_vkladok():
    vkladki = notebook.tabs()
    for tab_image in vkladki:
        notebook.forget(tab_image)

window = Tk()
window.title("Случайное изображение пёсика")
window.geometry("400x400")

status_label = ttk.Label(window, text="")
status_label.pack(padx=10, pady=5)


button = ttk.Button(window, text="Загрузить изображение пёсика", command=start_progress)
button.pack(padx=10, pady=10)

progress = ttk.Progressbar(window, mode='determinate', length=300)
progress.pack(padx=10, pady=5)

button_frame = ttk.Frame(window)
button_frame.pack(padx=10, pady=10)

ochistka_button = ttk.Button(button_frame, text="Очистить вкладки", command=ochistka_vkladok)
ochistka_button.pack(padx=10, pady=10)

width_label = ttk.Label(window, text="Ширина изображения:")
width_label.pack(side='left', padx=(10, 0))
width_spinbox = ttk.Spinbox(window, from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side='left', padx=(0, 10))
width_spinbox.set(350)

height_label = ttk.Label(window, text="Высота изображения:")
height_label.pack(side='left', padx=(10, 0))
height_spinbox = ttk.Spinbox(window, from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side='left', padx=(0, 10))
height_spinbox.set(350)


top_level_window = Toplevel(window)
top_level_window.title("Изображения пёсиков")

notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

window.mainloop()