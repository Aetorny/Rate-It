import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from savestate import SaveState

class RateItApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('Rate It')
        self.state = SaveState()
        self.data: dict[int, dict[str, str | int]] = self.state.load()
        self.keys: list[int] = list(self.data.keys())
        self.idx = 0
        self.selected_rating = tk.IntVar(value=0)
        self.photo_label = None
        self.radio_buttons: list[ttk.Radiobutton] = []
        self.setup_ui()
        self.show_photo()

    def setup_ui(self) -> None:
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Photo
        self.photo_label = ttk.Label(main_frame)
        self.photo_label.grid(row=0, column=0, rowspan=12, padx=10, pady=10)

        # Right: Radio buttons
        radio_frame = ttk.Frame(main_frame)
        radio_frame.grid(row=0, column=1, sticky='n')
        for i in range(1, 11):
            rb = ttk.Radiobutton(radio_frame, text=str(i), variable=self.selected_rating, value=i, command=self.on_rating_selected)
            rb.pack(anchor='w')
            self.radio_buttons.append(rb)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=11, column=1, sticky='s', pady=10)
        self.skip_btn = ttk.Button(btn_frame, text='Пропустить', command=self.skip_photo)
        self.skip_btn.pack(side=tk.LEFT, padx=5)
        self.next_btn = ttk.Button(btn_frame, text='Далее', command=self.save_rating, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Keyboard bindings
        self.root.bind('<Return>', lambda e: self.save_rating())
        self.root.bind('<KP_Enter>', lambda e: self.save_rating())
        self.root.bind('<space>', lambda e: self.skip_photo())
        for i in range(1, 10):
            self.root.bind(str(i), lambda e, v=i: self.select_rating(v))
        self.root.bind('0', lambda e: self.select_rating(10))

    def select_rating(self, value: int) -> None:
        if self.idx >= len(self.keys) or self.data[self.keys[self.idx]]['rating'] != 0:
            return
        self.selected_rating.set(value)
        self.on_rating_selected()

    def show_photo(self) -> None:
        while self.idx < len(self.keys) and self.data[self.keys[self.idx]]['rating'] != 0:
            self.idx += 1

        if self.idx >= len(self.keys):
            assert self.photo_label
            self.photo_label.config(text='Готово!', image='')
            for rb in self.radio_buttons:
                rb.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
            self.skip_btn.config(state=tk.DISABLED)
            return

        key = self.keys[self.idx]
        photo_path = self.data[key]['photo']
        assert isinstance(photo_path, str)
        img = Image.open(photo_path)

        max_size = 400, 400
        img.thumbnail(max_size, Image.LANCZOS) # type: ignore
        self.tk_img = ImageTk.PhotoImage(img)
        assert self.photo_label
        self.photo_label.config(image=self.tk_img, text='')
        self.selected_rating.set(0)
        self.next_btn.config(state=tk.DISABLED)

    def on_rating_selected(self) -> None:
        self.next_btn.config(state=tk.NORMAL)

    def save_rating(self) -> None:
        if self.idx >= len(self.keys) or self.data[self.keys[self.idx]]['rating'] != 0:
            return
        rating = self.selected_rating.get()
        if rating:
            key = self.keys[self.idx]
            self.data[key]['rating'] = rating
            self.state.save(self.data)
            self.idx += 1
            self.show_photo()

    def skip_photo(self) -> None:
        self.idx += 1
        self.show_photo()

if __name__ == '__main__':
    root = tk.Tk()
    app = RateItApp(root)
    root.mainloop()