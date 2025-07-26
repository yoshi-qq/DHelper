import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from os.path import join
from PIL import Image, ImageTk

from classes.types import Item, DamageType, AttributeType, Damage
from classes.textKeys import UIText, MessageText
from helpers.translationHelper import translate, to_enum
from config.constants import GAME, PATHS
from helpers.dataHelper import (
    getItems,
    addItem,
    updateItemCache,
    loadItemCache,
)
from handlers.imageHandler import ImageHandler


class InterfaceHandler:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(translate(UIText.APP_TITLE))
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
        style.configure(
            "TEntry",
            fieldbackground="#444",
            background="#444",
            foreground=fg,
            insertcolor=fg,
        )
        style.configure(
            "TCombobox",
            fieldbackground="#444",
            background="#444",
            foreground=fg,
            selectbackground="#555",
        )
        style.map("TButton", background=[("active", "#3a3a3a")])
        style.map("TCheckbutton", background=[("active", "#3a3a3a")])
        style.configure("Treeview", background="#444", foreground=fg, fieldbackground="#444")
        style.configure("Treeview.Heading", background="#555", foreground=fg)
        style.map("Treeview", background=[("selected", "#555")])
        self.root.configure(bg=dark_bg)

    def _clear_root(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()

    def _build_main_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(frame, text=translate(UIText.BUTTON_ITEMS), command=self._open_items_menu, width=30).pack(pady=10)
        ttk.Button(frame, text=translate(UIText.BUTTON_SPELLS), command=self._open_spells_menu, width=30).pack(pady=10)

    def _open_items_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(frame, text=translate(UIText.BUTTON_ADD_ITEM), command=self._open_add_item).pack(pady=5, fill="x")
        ttk.Button(frame, text=translate(UIText.BUTTON_MANAGE_ITEMS), command=self._open_manage_items).pack(pady=5, fill="x")
        ttk.Button(frame, text=translate(UIText.BUTTON_PRINT_ITEMS), command=self._open_print_items).pack(pady=5, fill="x")
        ttk.Button(frame, text=translate(UIText.BUTTON_BACK), command=self._build_main_menu).pack(pady=10)

    def _open_spells_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=translate(UIText.SPELLS_NOT_IMPLEMENTED)).pack(pady=10)
        ttk.Button(frame, text=translate(UIText.BUTTON_BACK), command=self._build_main_menu).pack(pady=10)

    # ===== Manage Items =====
    def _open_manage_items(self) -> None:
        window = tk.Toplevel(self.root)
        window.title(translate(UIText.MANAGE_ITEMS_TITLE))
        window.configure(bg=self.root["background"])

        items = getItems()

        search_var = tk.StringVar()
        sort_var = tk.StringVar(value=translate(UIText.COLUMN_ID))

        ttk.Label(window, text=translate(UIText.SEARCH_LABEL)).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        search_entry = ttk.Entry(window, textvariable=search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(window, text=translate(UIText.SORT_BY_LABEL)).grid(row=1, column=0, sticky="e", padx=5, pady=2)
        sort_map = {
            "id": UIText.COLUMN_ID,
            "name": UIText.COLUMN_NAME,
            "price": UIText.COLUMN_PRICE,
            "weight": UIText.COLUMN_WEIGHT,
        }
        sort_cb = ttk.Combobox(window, textvariable=sort_var, values=[translate(v) for v in sort_map.values()], state="readonly")
        sort_cb.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        attribute_types = [str(at) for at in AttributeType]
        attr_vars: dict[str, tk.BooleanVar] = {}
        attr_frame = ttk.Frame(window)
        attr_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
        for at in attribute_types:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(attr_frame, text=at, variable=var, command=lambda: update_list())
            chk.pack(side="left")
            attr_vars[at] = var

        columns = ("id", "name", "price", "weight")
        tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": UIText.COLUMN_ID,
            "name": UIText.COLUMN_NAME,
            "price": UIText.COLUMN_PRICE,
            "weight": UIText.COLUMN_WEIGHT,
        }
        for col in columns:
            tree.heading(col, text=translate(headings[col]))
            tree.column(col, width=100, anchor="center")
        tree.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        window.grid_rowconfigure(3, weight=1)
        window.grid_columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_VIEW_CARD), command=lambda: view_card()).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_EDIT_DATA), command=lambda: edit_selected()).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_EDIT_CARD), command=lambda: edit_card()).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_CLOSE), command=window.destroy).pack(side="left", padx=2)

        def filter_items() -> List[Item]:
            search = search_var.get().lower()
            selected = [to_enum(AttributeType, a) for a, v in attr_vars.items() if v.get()]
            filtered = []
            for it in items:
                if search not in it.name.lower() and search not in it.id.lower():
                    continue
                if selected and not all(a in it.attributes for a in selected):
                    continue
                filtered.append(it)
            return filtered

        def update_list(*_args: object) -> None:
            tree.delete(*tree.get_children())
            data = filter_items()
            reverse_map = {translate(v): k for k, v in sort_map.items()}
            key = reverse_map.get(sort_var.get(), "name")
            if key == "id":
                sort_key = lambda i: i.id
            elif key == "name":
                sort_key = lambda i: i.name
            elif key == "price":
                sort_key = lambda i: i.price
            elif key == "weight":
                sort_key = lambda i: i.weight
            else:
                sort_key = lambda i: i.name
            for it in sorted(data, key=sort_key):
                tree.insert("", "end", values=(it.id, it.name, it.price, it.weight))

        def get_selected_item() -> Item | None:
            sel = tree.selection()
            if not sel:
                return None
            item_id = tree.item(sel[0], "values")[0]
            for it in items:
                if it.id == item_id:
                    return it
            return None

        def view_card() -> None:
            item = get_selected_item()
            if not item:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            try:
                cache = loadItemCache()
                t = cache.get(item.id, {"rotate": 0.0, "scale": 1.0, "flip": False})
                self.image_handler.createItemCard(
                    item,
                    rotate=t.get("rotate", 0.0),
                    flip=t.get("flip", False),
                    scale=t.get("scale", 1.0),
                )
                path = join(PATHS.OUTPUT, f"{item.id}.png")
                img = Image.open(path)
                top = tk.Toplevel(window)
                top.title(f"{item.name} Card")
                tk_img = ImageTk.PhotoImage(img)
                lbl = ttk.Label(top, image=tk_img)
                lbl.image = tk_img # type: ignore (anti garbage collection)
                lbl.pack()
            except Exception as e:
                messagebox.showerror(
                    translate(MessageText.ERROR_TITLE),
                    str(e),
                )

        def edit_selected() -> None:
            item = get_selected_item()
            if not item:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            self._open_edit_item(item)
            items.clear()
            items.extend(getItems())
            update_list()

        def edit_card() -> None:
            item = get_selected_item()
            if not item:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            cache = loadItemCache()
            PreviewWindow(self.root, [item], self.image_handler, cache)

        search_var.trace_add("write", update_list)
        sort_cb.bind("<<ComboboxSelected>>", update_list)
        update_list()


    # ===== Add Item =====
    def _item_form(self, window: tk.Toplevel, item: Item | None) -> None:
        window.configure(bg=self.root["background"])

        entries: dict[str, tk.Entry] = {}
        row = 0
        labels = [UIText.COLUMN_ID, UIText.COLUMN_NAME, UIText.COLUMN_PRICE, UIText.COLUMN_WEIGHT]
        for label in labels:
            text = translate(label)
            ttk.Label(window, text=text).grid(row=row, column=0, sticky="e", padx=5, pady=2)
            entry = ttk.Entry(window)
            entry.grid(row=row, column=1, padx=5, pady=2)
            if item:
                match label:
                    case UIText.COLUMN_ID:
                        entry.insert(0, item.id)
                    case UIText.COLUMN_NAME:
                        entry.insert(0, item.name)
                    case UIText.COLUMN_PRICE:
                        entry.insert(0, str(item.price))
                    case UIText.COLUMN_WEIGHT:
                        entry.insert(0, str(item.weight))
            entries[text] = entry
            row += 1

        damage_types = [str(dt) for dt in DamageType]
        ttk.Label(window, text=translate(UIText.DAMAGE_LABEL)).grid(row=row, column=0, sticky="e", padx=5, pady=2)
        dmg_frame = ttk.Frame(window)
        dmg_frame.grid(row=row, column=1, sticky="w")
        entries["Damage Dice Amount"] = ttk.Entry(dmg_frame, width=4)
        entries["Damage Dice Amount"].pack(side="left")
        ttk.Label(dmg_frame, text="d").pack(side="left")
        dmg_dice_type = ttk.Combobox(dmg_frame, values=[str(d) for d in GAME.DICE_SIZES], width=4, state="readonly")
        dmg_dice_type.pack(side="left", padx=2)
        entries["Damage Dice Type"] = dmg_dice_type
        entries["Damage Bonus"] = ttk.Entry(dmg_frame, width=4)
        entries["Damage Bonus"].pack(side="left", padx=2)
        dmg_type_var = tk.StringVar(value="")
        dmg_type_cb = ttk.Combobox(dmg_frame, textvariable=dmg_type_var, values=[""] + damage_types, state="readonly", width=10)
        dmg_type_cb.pack(side="left", padx=2)
        if item and item.damage:
            entries["Damage Dice Amount"].insert(0, str(item.damage.diceAmount))
            dmg_dice_type.set(str(item.damage.diceType))
            entries["Damage Bonus"].insert(0, str(item.damage.bonus))
            dmg_type_var.set(str(item.damage.damageType))
        row += 1

        attribute_types = [str(at) for at in AttributeType]
        attr_vars: dict[str, tk.BooleanVar] = {}
        range_frames: dict[str, ttk.Frame] = {}
        range_entries: dict[str, tuple[tk.Entry, tk.Entry]] = {}
        ttk.Label(window, text=translate(UIText.ATTRIBUTES_LABEL)).grid(row=row, column=0, sticky="ne", padx=5, pady=2)
        attr_frame = ttk.Frame(window)
        attr_frame.grid(row=row, column=1, sticky="w")

        def toggle_range(at: str) -> None:
            frame = range_frames.get(at)
            if frame:
                if attr_vars[at].get():
                    frame.pack(anchor="w", padx=15)
                else:
                    frame.pack_forget()
            if at == translate(AttributeType.VERSATILE):
                if attr_vars[at].get():
                    vers_frame.grid()
                else:
                    vers_frame.grid_remove()

        for at in attribute_types:
            var = tk.BooleanVar(value=item is not None and to_enum(AttributeType, at) in item.attributes)
            chk = ttk.Checkbutton(attr_frame, text=at, variable=var, command=lambda a=at: toggle_range(a))
            chk.pack(anchor="w")
            attr_vars[at] = var
            if at in (translate(AttributeType.THROWN), translate(AttributeType.AMMUNITION)):
                r_frame = ttk.Frame(attr_frame)
                ttk.Label(r_frame, text="min").pack(side="left")
                e_min = ttk.Entry(r_frame, width=4)
                e_min.pack(side="left")
                ttk.Label(r_frame, text="/").pack(side="left")
                e_max = ttk.Entry(r_frame, width=4)
                e_max.pack(side="left")
                if item and to_enum(AttributeType, at) in item.ranges:
                    low, high = item.ranges[to_enum(AttributeType, at)]
                    e_min.insert(0, str(low))
                    e_max.insert(0, str(high))
                range_frames[at] = r_frame
                range_entries[at] = (e_min, e_max)
                if var.get():
                    r_frame.pack(anchor="w", padx=15)
        row += 1

        vers_frame = ttk.Frame(window)
        ttk.Label(vers_frame, text=translate(AttributeType.VERSATILE)).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        vers_inner = ttk.Frame(vers_frame)
        vers_inner.grid(row=0, column=1, sticky="w")
        entries["Versatile Dice Amount"] = ttk.Entry(vers_inner, width=4)
        entries["Versatile Dice Amount"].pack(side="left")
        ttk.Label(vers_inner, text="d").pack(side="left")
        vers_dice_type = ttk.Combobox(vers_inner, values=[str(d) for d in GAME.DICE_SIZES], width=4, state="readonly")
        vers_dice_type.pack(side="left", padx=2)
        entries["Versatile Dice Type"] = vers_dice_type
        entries["Versatile Damage Bonus"] = ttk.Entry(vers_inner, width=4)
        entries["Versatile Damage Bonus"].pack(side="left", padx=2)
        vers_frame.grid(row=row, column=0, columnspan=2, sticky="w")
        if item and item.versatileDamage:
            entries["Versatile Dice Amount"].insert(0, str(item.versatileDamage.diceAmount))
            vers_dice_type.set(str(item.versatileDamage.diceType))
            entries["Versatile Damage Bonus"].insert(0, str(item.versatileDamage.bonus))
        if item and AttributeType.VERSATILE in item.attributes:
            vers_frame.grid()
        else:
            vers_frame.grid_remove()
        row += 1

        def submit() -> None:
            try:
                _id = entries[translate(UIText.COLUMN_ID)].get().strip()
                name = entries[translate(UIText.COLUMN_NAME)].get().strip()
                price = float(entries[translate(UIText.COLUMN_PRICE)].get()) if entries[translate(UIText.COLUMN_PRICE)].get() else 0
                weight = float(entries[translate(UIText.COLUMN_WEIGHT)].get()) if entries[translate(UIText.COLUMN_WEIGHT)].get() else 0
                dmg_amount = int(entries["Damage Dice Amount"].get()) if entries["Damage Dice Amount"].get() else 0
                dmg_type = int(entries["Damage Dice Type"].get()) if entries["Damage Dice Type"].get() else 1
                dmg_bonus = int(entries["Damage Bonus"].get()) if entries["Damage Bonus"].get() else 0
                vers_amount = int(entries["Versatile Dice Amount"].get()) if entries["Versatile Dice Amount"].get() else 0
                vers_type = int(entries["Versatile Dice Type"].get()) if entries["Versatile Dice Type"].get() else 1
                vers_bonus = int(entries["Versatile Damage Bonus"].get()) if entries["Versatile Damage Bonus"].get() else 0
                damage_type = to_enum(DamageType, dmg_type_var.get()) if dmg_type_var.get() else None
                attributes = [to_enum(AttributeType, at) for at in attribute_types if attr_vars[at].get()]
                ranges: dict[AttributeType, tuple[int, int]] = {}
                for at in (translate(AttributeType.THROWN), translate(AttributeType.AMMUNITION)):
                    if attr_vars.get(at) and attr_vars[at].get():
                        try:
                            low = int(range_entries[at][0].get())
                            high = int(range_entries[at][1].get())
                        except ValueError:
                            messagebox.showerror(
                                translate(MessageText.ERROR_TITLE),
                                translate(MessageText.INVALID_RANGE).format(attr=at),
                            )
                            return
                        ranges[to_enum(AttributeType, at)] = (low, high)
            except ValueError as e:
                messagebox.showerror(
                    translate(MessageText.ERROR_TITLE),
                    translate(MessageText.INVALID_VALUE).format(error=e),
                )
                return
            if not _id or not name:
                messagebox.showerror(
                    translate(MessageText.ERROR_TITLE),
                    translate(MessageText.ID_NAME_REQUIRED),
                )
                return
            new_item = Item(
                _id=_id,
                name=name,
                price=price,
                weight=weight,
                damageDiceAmount=dmg_amount,
                damageDiceType=dmg_type,
                damageBonus=dmg_bonus,
                damageType=damage_type,
                versatileDamage=(
                    Damage(
                        vers_amount,
                        vers_type,
                        vers_bonus,
                        to_enum(DamageType, dmg_type_var.get()) if dmg_type_var.get() else (damage_type if damage_type is not None else DamageType.SLASHING)
                    )
                    if (vers_amount or vers_bonus) and (dmg_type_var.get() or damage_type)
                    else None
                ),
                attributes=attributes,
                ranges=ranges,
            )
            addItem(new_item)
            messagebox.showinfo(
                translate(MessageText.SAVED_TITLE),
                translate(MessageText.ITEM_SAVED),
            )
            window.destroy()

        ttk.Button(window, text=translate(UIText.SAVE_BUTTON), command=submit).grid(row=row, column=0, columnspan=2, pady=10)

    def _open_add_item(self) -> None:
        window = tk.Toplevel(self.root)
        window.title(translate(UIText.ADD_ITEM_TITLE))
        self._item_form(window, None)

    def _open_edit_item(self, item: Item) -> None:
        window = tk.Toplevel(self.root)
        window.title(f"{translate(UIText.EDIT_ITEM_TITLE)}: {item.name}")
        self._item_form(window, item)

    # ===== Print Items =====
    def _open_print_items(self) -> None:
        items = getItems()
        if not items:
            messagebox.showinfo(
                translate(MessageText.NO_ITEMS_TITLE),
                translate(MessageText.NO_ITEMS_MESSAGE),
            )
            return

        cache = loadItemCache()
        show_all = messagebox.askyesno(
            translate(MessageText.PREVIEW_MODE),
            translate(MessageText.PREVIEW_QUESTION),
        )
        preview_items: List[Item] = []
        for item in items:
            if show_all or item.id not in cache:
                preview_items.append(item)
            else:
                t = cache[item.id]
                self.image_handler.createItemCard(
                    item,
                    rotate=t.get("rotate", 0.0),
                    flip=t.get("flip", False),
                    scale=t.get("scale", 1.0),
                )

        if preview_items:
            PreviewWindow(self.root, preview_items, self.image_handler, cache)
        else:
            messagebox.showinfo(
                translate(MessageText.DONE_TITLE),
                translate(MessageText.DONE_MESSAGE),
            )

    def run(self) -> None:
        self.root.mainloop()


class PreviewWindow(tk.Toplevel):
    def __init__(
        self,
        root: tk.Tk,
        items: List[Item],
        image_handler: ImageHandler,
        cache: dict,
    ) -> None:
        super().__init__(root)
        self.title(translate(UIText.ITEM_PREVIEW_TITLE))
        self.configure(bg=root["background"])
        self.items = items
        self.index = 0
        self.image_handler = image_handler
        self.cache = cache
        self.skipped: set[str] = set()
        self.label = ttk.Label(self)
        self.label.pack(padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack()
        self.angle_var = tk.DoubleVar(value=0)
        ttk.Scale(btn_frame, from_=-180, to=180, orient="horizontal", variable=self.angle_var, command=self._update_angle, length=150).pack(side="left", padx=2)
        self.scale_var = tk.DoubleVar(value=1.0)
        ttk.Scale(btn_frame, from_=0.5, to=1.5, orient="horizontal", variable=self.scale_var, command=self._update_scale, length=150).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_FLIP), command=self._toggle_flip).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_SKIP), command=self._skip).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=translate(UIText.BUTTON_NEXT), command=self._next).pack(side="left", padx=2)
        self.flip = False
        self.skip_flag = False

        self.original: Image.Image | None = None
        self.display: Image.Image | None = None
        self.tk_img: ImageTk.PhotoImage | None = None
        self._load_current()

    def _load_current(self) -> None:
        item = self.items[self.index]
        t = self.cache.get(item.id, {"rotate": 0.0, "scale": 1.0, "flip": False})
        self.angle_var.set(t.get("rotate", 0.0))
        self.scale_var.set(t.get("scale", 1.0))
        self.flip = t.get("flip", False)
        if not self._generate_image(item):
            return
        self._update_image()

    def _generate_image(self, item: Item) -> bool:
        try:
            self.image_handler.createItemCard(
                item,
                rotate=self.angle_var.get(),
                flip=self.flip,
                scale=self.scale_var.get(),
            )
        except FileNotFoundError:
            if messagebox.askretrycancel(
                translate(MessageText.MISSING_IMAGE_TITLE),
                translate(MessageText.MISSING_IMAGE_MESSAGE).format(id=item.id),
            ):
                return self._generate_image(item)
            else:
                self.skip_flag = True
                return False
        path = join(PATHS.OUTPUT, f"{item.id}.png")
        self.original = Image.open(path)
        self.display = self.original
        return True

    def _update_image(self) -> None:
        if self.display is None:
            return
        self.tk_img = ImageTk.PhotoImage(self.display)
        self.label.configure(image=self.tk_img)

    def _update_scale(self, _value: str) -> None:
        self._apply_transform()

    def _update_angle(self, _value: str) -> None:
        self._apply_transform()

    def _toggle_flip(self) -> None:
        self.flip = not self.flip
        self._apply_transform()

    def _apply_transform(self) -> None:
        item = self.items[self.index]
        if not self._generate_image(item):
            return
        self._update_image()

    def _next(self) -> None:
        item = self.items[self.index]
        if not self.skip_flag:
            updateItemCache(
                item.id,
                self.angle_var.get(),
                self.scale_var.get(),
                self.flip,
            )
        self.skip_flag = False
        self.index += 1
        if self.index >= len(self.items):
            self.destroy()
            return
        self._load_current()

    def _skip(self) -> None:
        self.skip_flag = True
        self._next()

