import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from os.path import join
from PIL import Image, ImageTk

from classes.types import Item, DamageType, AttributeType
from config.constants import OUTPUT_PATH
from helpers.dataHelper import getItems, addItem
from handlers.imageHandler import ImageHandler


class InterfaceHandler:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("DHelper")
        self._set_dark_theme()
        self.image_handler = ImageHandler()
        self._build_main_menu()

    def _set_dark_theme(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        dark_bg = "#2b2b2b"
        fg = "#f0f0f0"
        style.configure(".", background=dark_bg, foreground=fg)
        style.configure("TFrame", background=dark_bg)
        style.configure("TLabel", background=dark_bg, foreground=fg)
        style.configure("TCheckbutton", background=dark_bg, foreground=fg)
        style.configure("TButton", background="#444", foreground=fg)
        style.map("TButton", background=[("active", "#555")])
        self.root.configure(bg=dark_bg)

    def _clear_root(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()

    def _build_main_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(frame, text="Items", command=self._open_items_menu, width=30).pack(pady=10)
        ttk.Button(frame, text="Spells", command=self._open_spells_menu, width=30).pack(pady=10)

    def _open_items_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(frame, text="Add Item", command=self._open_add_item).pack(pady=5, fill="x")
        ttk.Button(frame, text="Print Items", command=self._open_print_items).pack(pady=5, fill="x")
        ttk.Button(frame, text="Back", command=self._build_main_menu).pack(pady=10)

    def _open_spells_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Spells functionality not implemented yet").pack(pady=10)
        ttk.Button(frame, text="Back", command=self._build_main_menu).pack(pady=10)

    # ===== Add Item =====
    def _open_add_item(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Add Item")
        window.configure(bg=self.root["background"])

        entries: dict[str, tk.Entry] = {}
        row = 0
        for label in ["ID", "Name", "Price", "Weight", "Damage Dice Amount", "Damage Dice Type", "Damage Bonus"]:
            ttk.Label(window, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=2)
            entry = ttk.Entry(window)
            entry.grid(row=row, column=1, padx=5, pady=2)
            entries[label] = entry
            row += 1

        damage_types = list(DamageType.__args__)  # type: ignore
        ttk.Label(window, text="Damage Type").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        dmg_type_var = tk.StringVar(value="")
        ttk.Combobox(window, textvariable=dmg_type_var, values=[""] + damage_types, state="readonly").grid(row=row, column=1, padx=5, pady=2)
        row += 1

        attribute_types = list(AttributeType.__args__)  # type: ignore
        attr_vars: List[tk.BooleanVar] = []
        ttk.Label(window, text="Attributes").grid(row=row, column=0, sticky="ne", padx=5, pady=2)
        attr_frame = ttk.Frame(window)
        attr_frame.grid(row=row, column=1, sticky="w")
        for at in attribute_types:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(attr_frame, text=at, variable=var)
            chk.pack(anchor="w")
            attr_vars.append(var)
        row += 1

        def submit() -> None:
            try:
                _id = entries["ID"].get().strip()
                name = entries["Name"].get().strip()
                price = float(entries["Price"].get()) if entries["Price"].get() else 0
                weight = float(entries["Weight"].get()) if entries["Weight"].get() else 0
                dmg_amount = int(entries["Damage Dice Amount"].get()) if entries["Damage Dice Amount"].get() else 0
                dmg_type = int(entries["Damage Dice Type"].get()) if entries["Damage Dice Type"].get() else 1
                dmg_bonus = int(entries["Damage Bonus"].get()) if entries["Damage Bonus"].get() else 0
                damage_type = dmg_type_var.get() or None
                attributes = [at for at, var in zip(attribute_types, attr_vars) if var.get()]
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid value: {e}")
                return
            if not _id or not name:
                messagebox.showerror("Error", "ID and Name are required")
                return
            item = Item(
                _id=_id,
                name=name,
                price=price,
                weight=weight,
                damageDiceAmount=dmg_amount,
                damageDiceType=dmg_type,
                damageBonus=dmg_bonus,
                damageType=damage_type,  # type: ignore
                attributes=attributes,
            )
            addItem(item)
            messagebox.showinfo("Saved", "Item saved")
            window.destroy()

        ttk.Button(window, text="Add", command=submit).grid(row=row, column=0, columnspan=2, pady=10)

    # ===== Print Items =====
    def _open_print_items(self) -> None:
        items = getItems()
        if not items:
            messagebox.showinfo("No Items", "No items found")
            return
        PreviewWindow(self.root, items, self.image_handler)

    def run(self) -> None:
        self.root.mainloop()


class PreviewWindow(tk.Toplevel):
    def __init__(self, root: tk.Tk, items: List[Item], image_handler: ImageHandler) -> None:
        super().__init__(root)
        self.title("Item Preview")
        self.configure(bg=root["background"])
        self.items = items
        self.index = 0
        self.image_handler = image_handler
        self.label = ttk.Label(self)
        self.label.pack(padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack()
        self.angle_var = tk.DoubleVar(value=0)
        ttk.Scale(btn_frame, from_=-180, to=180, orient="horizontal", variable=self.angle_var, command=self._update_angle, length=150).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Flip", command=self._toggle_flip).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Next", command=self._next).pack(side="left", padx=2)
        self.flip = False

        self.original: Image.Image | None = None
        self.display: Image.Image | None = None
        self.tk_img: ImageTk.PhotoImage | None = None
        self._load_current()

    def _load_current(self) -> None:
        item = self.items[self.index]
        self.angle_var.set(0)
        self.flip = False
        self.image_handler.createItemCard(item)
        path = join(OUTPUT_PATH, f"{item.id}.png")
        self.original = Image.open(path)
        self.display = self.original
        self._update_image()

    def _update_image(self) -> None:
        if self.display is None:
            return
        self.tk_img = ImageTk.PhotoImage(self.display)
        self.label.configure(image=self.tk_img)

    def _update_angle(self, _value: str) -> None:
        self._apply_transform()

    def _toggle_flip(self) -> None:
        self.flip = not self.flip
        self._apply_transform()

    def _apply_transform(self) -> None:
        item = self.items[self.index]
        angle = self.angle_var.get()
        self.image_handler.createItemCard(item, rotate=angle, flip=self.flip)
        path = join(OUTPUT_PATH, f"{item.id}.png")
        self.display = Image.open(path)
        self._update_image()

    def _next(self) -> None:
        self.index += 1
        if self.index >= len(self.items):
            self.destroy()
            return
        self._load_current()