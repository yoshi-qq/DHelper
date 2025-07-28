import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Sequence, Union
from datetime import timedelta
import os
from os.path import join
from PIL import Image, ImageTk

from classes.types import (
    Item,
    Weapon,
    Armor,
    SimpleItem,
    ArmorCategory,
    DamageType,
    AttributeType,
    Damage,
    Spell,
    SpellType,
    CasterClassType,
    CastingTimeType,
    TargetType,
    Material,
    Components,
    ItemCache,
    SpellCache,
)
from classes.textKeys import UIText, MessageText
from helpers.translationHelper import (
    translate,
    to_enum,
    get_language,
    set_language,
    set_theme,
    get_theme,
    get_skip_missing,
    set_skip_missing,
    LANG_DIR,
)
from config.constants import GAME, PATHS, IMAGE
from helpers.dataHelper import (
    getWeapons,
    addWeapon,
    getArmors,
    addArmor,
    getItems,
    addItem,
    updateItemCache,
    loadItemCache,
    getSpells,
    addSpell,
    loadSpellCache,
    updateSpellCache,
)
from handlers.imageHandler import ImageHandler


class InterfaceHandler:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(translate(UIText.APP_TITLE))
        self._set_icon(self.root)
        self._apply_theme()
        self.image_handler = ImageHandler()
        self._build_main_menu()

    def _set_icon(self, window: tk.Toplevel | tk.Tk) -> None:
        try:
            icon = tk.PhotoImage(file=IMAGE.PATHS.APP_ICON)
            window.iconphoto(True, icon)
        except Exception:
            pass

    def _set_modern_theme(self) -> None:
        style: ttk.Style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        bg = "#f5f5f5"
        fg = "#333333"
        style.configure(".", background=bg, foreground=fg)  # type: ignore
        style.configure("TFrame", background=bg)  # type: ignore
        style.configure("TLabel", background=bg, foreground=fg)  # type: ignore
        style.configure("TCheckbutton", background=bg, foreground=fg)  # type: ignore
        style.configure("TButton", background="#e0e0e0", foreground=fg)  # type: ignore
        style.configure(  # type: ignore
            "TEntry",
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground=fg,
            insertcolor=fg,
        )
        style.configure(  # type: ignore
            "TCombobox",
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground=fg,
            selectbackground="#dddddd",
        )
        self.root.option_add("*TCombobox*Listbox.background", "#ffffff")  # type: ignore
        self.root.option_add("*TCombobox*Listbox.foreground", fg)  # type: ignore
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#dddddd")  # type: ignore
        style.map("TButton", background=[("active", "#cccccc")])  # type: ignore
        style.map("TCheckbutton", background=[("active", "#cccccc")])  # type: ignore
        style.configure("Treeview", background="#ffffff", foreground=fg, fieldbackground="#ffffff")  # type: ignore
        style.configure("Treeview.Heading", background="#e0e0e0", foreground=fg)  # type: ignore
        style.map("Treeview", background=[("selected", "#cccccc")])  # type: ignore
        self.root.configure(bg=bg)

    def _set_dark_theme(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        bg = "#333333"
        fg = "#f5f5f5"
        style.configure(".", background=bg, foreground=fg)  # type: ignore
        style.configure("TFrame", background=bg)  # type: ignore
        style.configure("TLabel", background=bg, foreground=fg)  # type: ignore
        style.configure("TCheckbutton", background=bg, foreground=fg)  # type: ignore
        style.configure("TButton", background="#444444", foreground=fg)  # type: ignore
        style.configure(  # type: ignore
            "TEntry",
            fieldbackground="#555555",
            background="#555555",
            foreground=fg,
            insertcolor=fg,
        )
        style.configure(  # type: ignore
            "TCombobox",
            fieldbackground="#555555",
            background="#555555",
            foreground=fg,
            selectbackground="#666666",
        )
        self.root.option_add("*TCombobox*Listbox.background", "#555555")  # type: ignore
        self.root.option_add("*TCombobox*Listbox.foreground", fg)  # type: ignore
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#777777")  # type: ignore
        style.map("TButton", background=[("active", "#666666")])  # type: ignore
        style.map("TCheckbutton", background=[("active", "#666666")])  # type: ignore
        style.configure("Treeview", background="#555555", foreground=fg, fieldbackground="#555555")  # type: ignore
        style.configure("Treeview.Heading", background="#444444", foreground=fg)  # type: ignore
        style.map("Treeview", background=[("selected", "#666666")])  # type: ignore
        self.root.configure(bg=bg)

    def _apply_theme(self) -> None:
        if get_theme() == "dark":
            self._set_dark_theme()
        else:
            self._set_modern_theme()

    def _clear_root(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()

    def _build_main_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_WEAPONS),
            command=self._open_weapons_menu,
            width=30,
        ).pack(pady=10)
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_ARMOR),
            command=self._open_armors_menu,
            width=30,
        ).pack(pady=10)
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_ITEMS),
            command=self._open_items_menu,
            width=30,
        ).pack(pady=10)
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_SPELLS),
            command=self._open_spells_menu,
            width=30,
        ).pack(pady=10)
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_SETTINGS),
            command=self._open_settings_menu,
            width=30,
        ).pack(pady=10)

    def _open_weapons_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(
            frame, text=translate(UIText.BUTTON_ADD_ITEM), command=self._open_add_weapon
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_MANAGE_ITEMS),
            command=self._open_manage_weapons,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_PRINT_ITEMS),
            command=self._open_print_weapons,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame, text=translate(UIText.BUTTON_BACK), command=self._build_main_menu
        ).pack(pady=10)

    def _open_armors_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(
            frame, text=translate(UIText.BUTTON_ADD_ITEM), command=self._open_add_armor
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_MANAGE_ITEMS),
            command=self._open_manage_armors,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_PRINT_ITEMS),
            command=self._open_print_armors,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame, text=translate(UIText.BUTTON_BACK), command=self._build_main_menu
        ).pack(pady=10)

    def _open_items_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(
            frame, text=translate(UIText.BUTTON_ADD_ITEM), command=self._open_add_item
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_MANAGE_ITEMS),
            command=self._open_manage_items,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_PRINT_ITEMS),
            command=self._open_print_items,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame, text=translate(UIText.BUTTON_BACK), command=self._build_main_menu
        ).pack(pady=10)

    def _open_spells_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Button(
            frame, text=translate(UIText.BUTTON_ADD_SPELL), command=self._open_add_spell
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_MANAGE_SPELLS),
            command=self._open_manage_spells,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame,
            text=translate(UIText.BUTTON_PRINT_SPELLS),
            command=self._open_print_spells,
        ).pack(pady=5, fill="x")
        ttk.Button(
            frame, text=translate(UIText.BUTTON_BACK), command=self._build_main_menu
        ).pack(pady=10)

    def _open_settings_menu(self) -> None:
        self._clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=translate(UIText.LANGUAGE_LABEL)).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        languages = [f[:-5] for f in os.listdir(LANG_DIR) if f.endswith(".json")]
        lang_var = tk.StringVar(value=get_language())
        ttk.Combobox(
            frame, textvariable=lang_var, values=languages, state="readonly"
        ).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text=translate(UIText.THEME_LABEL)).grid(
            row=1, column=0, sticky="e", padx=5, pady=2
        )
        theme_map = {"light": UIText.LIGHT_OPTION, "dark": UIText.DARK_OPTION}
        theme_var = tk.StringVar(value=translate(theme_map[get_theme()]))
        ttk.Combobox(
            frame,
            textvariable=theme_var,
            values=[translate(v) for v in theme_map.values()],
            state="readonly",
        ).grid(row=1, column=1, padx=5, pady=2)

        skip_var = tk.BooleanVar(value=get_skip_missing())
        ttk.Checkbutton(
            frame,
            text=translate(UIText.SKIP_MISSING_LABEL),
            variable=skip_var,
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=2)

        def apply() -> None:
            set_language(lang_var.get())
            reverse = {translate(v): k for k, v in theme_map.items()}
            set_theme(reverse.get(theme_var.get(), "light"))
            set_skip_missing(skip_var.get())
            self._apply_theme()
            self._build_main_menu()

        ttk.Button(frame, text=translate(UIText.SAVE_BUTTON), command=apply).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    # ===== Manage Weapons =====
    def _open_manage_weapons(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.MANAGE_ITEMS_TITLE))
        window.configure(bg=self.root["background"])

        items = getWeapons()

        search_var = tk.StringVar()
        sort_var = tk.StringVar(value=translate(UIText.COLUMN_ID))

        ttk.Label(window, text=translate(UIText.SEARCH_LABEL)).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        search_entry = ttk.Entry(window, textvariable=search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(window, text=translate(UIText.SORT_BY_LABEL)).grid(
            row=1, column=0, sticky="e", padx=5, pady=2
        )
        sort_map = {
            "id": UIText.COLUMN_ID,
            "name": UIText.COLUMN_NAME,
            "price": UIText.COLUMN_PRICE,
            "weight": UIText.COLUMN_WEIGHT,
        }
        sort_cb = ttk.Combobox(
            window,
            textvariable=sort_var,
            values=[translate(v) for v in sort_map.values()],
            state="readonly",
        )
        sort_cb.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        attribute_types = [str(at) for at in AttributeType]
        attr_vars: dict[str, tk.BooleanVar] = {}
        attr_frame = ttk.Frame(window)
        attr_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
        for at in attribute_types:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(
                attr_frame, text=at, variable=var, command=lambda: update_list()
            )
            chk.pack(side="left")
            attr_vars[at] = var

        columns = ("id", "name", "price", "weight")
        tree = ttk.Treeview(
            window, columns=columns, show="headings", selectmode="browse"
        )
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
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_VIEW_CARD),
            command=lambda: view_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_DATA),
            command=lambda: edit_selected(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_CARD),
            command=lambda: edit_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_CLOSE), command=window.destroy
        ).pack(side="left", padx=2)

        def filter_items() -> List[Item]:
            search = search_var.get().lower()
            selected = [
                to_enum(AttributeType, a) for a, v in attr_vars.items() if v.get()
            ]
            filtered: List[Item] = []
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
            sort_key: Callable[[Item], object]
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
                cache: ItemCache = loadItemCache()
                t = cache.get(item.id, {"rotate": 0.0, "scale": 1.0, "flip": False})
                self.image_handler.createItemCard(
                    item,
                    rotate=t.get("rotate", 0.0),
                    flip=bool(t.get("flip", False)),
                    scale=t.get("scale", 1.0),
                    offset_x=t.get("offset_x", 0.0),
                    offset_y=t.get("offset_y", 0.0),
                )
                path = self.image_handler.getItemOutputPath(item)
                img = Image.open(path)
                top = tk.Toplevel(window)
                self._set_icon(top)
                top.title(f"{item.name} Card")
                tk_img = ImageTk.PhotoImage(img)
                lbl = ttk.Label(top, image=tk_img)
                lbl.image = tk_img  # type: ignore (anti garbage collection)
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
            self._open_edit_weapon(item)
            items.clear()
            items.extend(getWeapons())
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

    def _open_manage_items(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.MANAGE_ITEMS_TITLE))
        window.configure(bg=self.root["background"])

        items = getItems()

        search_var = tk.StringVar()
        ttk.Label(window, text=translate(UIText.SEARCH_LABEL)).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        ttk.Entry(window, textvariable=search_var).grid(
            row=0, column=1, sticky="ew", padx=5, pady=2
        )

        tree = ttk.Treeview(
            window,
            columns=("id", "name", "price", "weight"),
            show="headings",
            selectmode="browse",
        )
        for col, key in zip(
            ("id", "name", "price", "weight"),
            [
                UIText.COLUMN_ID,
                UIText.COLUMN_NAME,
                UIText.COLUMN_PRICE,
                UIText.COLUMN_WEIGHT,
            ],
        ):
            tree.heading(col, text=translate(key))
            tree.column(col, width=100, anchor="center")
        tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_VIEW_CARD),
            command=lambda: view_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_DATA),
            command=lambda: edit_selected(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_CARD),
            command=lambda: edit_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_CLOSE), command=window.destroy
        ).pack(side="left", padx=2)

        def filter_items() -> List[SimpleItem]:
            search = search_var.get().lower()
            return [
                it
                for it in items
                if search in it.id.lower() or search in it.name.lower()
            ]

        def update_list(*_args: object) -> None:
            tree.delete(*tree.get_children())
            for it in filter_items():
                tree.insert("", "end", values=(it.id, it.name, it.price, it.weight))

        def get_selected_item() -> SimpleItem | None:
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
            cache = loadItemCache()
            PreviewWindow(self.root, [item], self.image_handler, cache)

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
        update_list()

    def _open_manage_armors(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.MANAGE_ITEMS_TITLE))
        window.configure(bg=self.root["background"])

        items = getArmors()

        search_var = tk.StringVar()
        ttk.Label(window, text=translate(UIText.SEARCH_LABEL)).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        ttk.Entry(window, textvariable=search_var).grid(
            row=0, column=1, sticky="ew", padx=5, pady=2
        )

        tree = ttk.Treeview(
            window, columns=("id", "name", "ac"), show="headings", selectmode="browse"
        )
        tree.heading("id", text=translate(UIText.COLUMN_ID))
        tree.heading("name", text=translate(UIText.COLUMN_NAME))
        tree.heading("ac", text="AC")
        for col in ("id", "name", "ac"):
            tree.column(col, width=100, anchor="center")
        tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_VIEW_CARD),
            command=lambda: view_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_DATA),
            command=lambda: edit_selected(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_CARD),
            command=lambda: edit_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_CLOSE), command=window.destroy
        ).pack(side="left", padx=2)

        def filter_items() -> List[Armor]:
            search = search_var.get().lower()
            return [
                it
                for it in items
                if search in it.id.lower() or search in it.name.lower()
            ]

        def update_list(*_args: object) -> None:
            tree.delete(*tree.get_children())
            for it in filter_items():
                tree.insert("", "end", values=(it.id, it.name, it.armorClass))

        def get_selected_item() -> Armor | None:
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
            cache = loadItemCache()
            PreviewWindow(self.root, [item], self.image_handler, cache)

        def edit_selected() -> None:
            item = get_selected_item()
            if not item:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            self._open_edit_armor(item)
            items.clear()
            items.extend(getArmors())
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
        update_list()

    # ===== Add Item =====
    def _item_form(self, window: tk.Toplevel, item: Item | None) -> None:
        self._set_icon(window)
        window.configure(bg=self.root["background"])

        entries: dict[str, tk.Entry] = {}
        row = 0
        labels = [
            UIText.COLUMN_ID,
            UIText.COLUMN_NAME,
            UIText.COLUMN_PRICE,
            UIText.COLUMN_WEIGHT,
        ]
        for label in labels:
            text = translate(label)
            ttk.Label(window, text=text).grid(
                row=row, column=0, sticky="e", padx=5, pady=2
            )
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
                    case _:
                        pass
            entries[text] = entry
            row += 1

        damage_types = [str(dt) for dt in DamageType]
        ttk.Label(window, text=translate(UIText.DAMAGE_LABEL)).grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dmg_frame = ttk.Frame(window)
        dmg_frame.grid(row=row, column=1, sticky="w")
        entries["Damage Dice Amount"] = ttk.Entry(dmg_frame, width=4)
        entries["Damage Dice Amount"].pack(side="left")
        ttk.Label(dmg_frame, text="d").pack(side="left")
        dmg_dice_type = ttk.Combobox(
            dmg_frame,
            values=[str(d) for d in GAME.DICE_SIZES],
            width=4,
            state="readonly",
        )
        dmg_dice_type.pack(side="left", padx=2)
        entries["Damage Dice Type"] = dmg_dice_type
        entries["Damage Bonus"] = ttk.Entry(dmg_frame, width=4)
        entries["Damage Bonus"].pack(side="left", padx=2)
        dmg_type_var = tk.StringVar(value="")
        dmg_type_cb = ttk.Combobox(
            dmg_frame,
            textvariable=dmg_type_var,
            values=[""] + damage_types,
            state="readonly",
            width=10,
        )
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
        ttk.Label(window, text=translate(UIText.ATTRIBUTES_LABEL)).grid(
            row=row, column=0, sticky="ne", padx=5, pady=2
        )
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
            var = tk.BooleanVar(
                value=item is not None and to_enum(AttributeType, at) in item.attributes
            )
            chk = ttk.Checkbutton(
                attr_frame, text=at, variable=var, command=lambda a=at: toggle_range(a)
            )
            chk.pack(anchor="w")
            attr_vars[at] = var
            if at in (
                translate(AttributeType.THROWN),
                translate(AttributeType.AMMUNITION),
            ):
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
        ttk.Label(vers_frame, text=translate(AttributeType.VERSATILE)).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        vers_inner = ttk.Frame(vers_frame)
        vers_inner.grid(row=0, column=1, sticky="w")
        entries["Versatile Dice Amount"] = ttk.Entry(vers_inner, width=4)
        entries["Versatile Dice Amount"].pack(side="left")
        ttk.Label(vers_inner, text="d").pack(side="left")
        vers_dice_type = ttk.Combobox(
            vers_inner,
            values=[str(d) for d in GAME.DICE_SIZES],
            width=4,
            state="readonly",
        )
        vers_dice_type.pack(side="left", padx=2)
        entries["Versatile Dice Type"] = vers_dice_type
        entries["Versatile Damage Bonus"] = ttk.Entry(vers_inner, width=4)
        entries["Versatile Damage Bonus"].pack(side="left", padx=2)
        vers_frame.grid(row=row, column=0, columnspan=2, sticky="w")
        if item and item.versatileDamage:
            entries["Versatile Dice Amount"].insert(
                0, str(item.versatileDamage.diceAmount)
            )
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
                price = (
                    float(entries[translate(UIText.COLUMN_PRICE)].get())
                    if entries[translate(UIText.COLUMN_PRICE)].get()
                    else 0
                )
                weight = (
                    float(entries[translate(UIText.COLUMN_WEIGHT)].get())
                    if entries[translate(UIText.COLUMN_WEIGHT)].get()
                    else 0
                )
                dmg_amount = (
                    int(entries["Damage Dice Amount"].get())
                    if entries["Damage Dice Amount"].get()
                    else 0
                )
                dmg_type = (
                    int(entries["Damage Dice Type"].get())
                    if entries["Damage Dice Type"].get()
                    else 1
                )
                dmg_bonus = (
                    int(entries["Damage Bonus"].get())
                    if entries["Damage Bonus"].get()
                    else 0
                )
                vers_amount = (
                    int(entries["Versatile Dice Amount"].get())
                    if entries["Versatile Dice Amount"].get()
                    else 0
                )
                vers_type = (
                    int(entries["Versatile Dice Type"].get())
                    if entries["Versatile Dice Type"].get()
                    else 1
                )
                vers_bonus = (
                    int(entries["Versatile Damage Bonus"].get())
                    if entries["Versatile Damage Bonus"].get()
                    else 0
                )
                damage_type = (
                    to_enum(DamageType, dmg_type_var.get())
                    if dmg_type_var.get()
                    else None
                )
                attributes = [
                    to_enum(AttributeType, at)
                    for at in attribute_types
                    if attr_vars[at].get()
                ]
                ranges: dict[AttributeType, tuple[int, int]] = {}
                for at in (
                    translate(AttributeType.THROWN),
                    translate(AttributeType.AMMUNITION),
                ):
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
                        (
                            to_enum(DamageType, dmg_type_var.get())
                            if dmg_type_var.get()
                            else (
                                damage_type
                                if damage_type is not None
                                else DamageType.SLASHING
                            )
                        ),
                    )
                    if (vers_amount or vers_bonus)
                    and (dmg_type_var.get() or damage_type)
                    else None
                ),
                attributes=attributes,
                ranges=ranges,
            )
            addWeapon(
                Weapon(
                    _id=new_item.id,
                    name=new_item.name,
                    price=new_item.price,
                    weight=new_item.weight,
                    damageDiceAmount=dmg_amount,
                    damageDiceType=dmg_type,
                    damageBonus=dmg_bonus,
                    damageType=damage_type,
                    versatileDamage=new_item.versatileDamage,
                    attributes=new_item.attributes,
                    ranges=new_item.ranges,
                )
            )
            messagebox.showinfo(
                translate(MessageText.SAVED_TITLE),
                translate(MessageText.ITEM_SAVED),
            )
            window.destroy()

        ttk.Button(window, text=translate(UIText.SAVE_BUTTON), command=submit).grid(
            row=row, column=0, columnspan=2, pady=10
        )

    def _simple_item_form(self, window: tk.Toplevel, item: SimpleItem | None) -> None:
        self._set_icon(window)
        window.configure(bg=self.root["background"])

        entries: dict[str, tk.Entry] = {}
        row = 0
        labels = [
            UIText.COLUMN_ID,
            UIText.COLUMN_NAME,
            UIText.COLUMN_PRICE,
            UIText.COLUMN_WEIGHT,
        ]
        for label in labels:
            text = translate(label)
            ttk.Label(window, text=text).grid(
                row=row, column=0, sticky="e", padx=5, pady=2
            )
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
                    case _:
                        pass
            entries[text] = entry
            row += 1

        ttk.Label(window, text="Description").grid(
            row=row, column=0, sticky="ne", padx=5, pady=2
        )
        desc = tk.Text(window, width=30, height=4)
        desc.grid(row=row, column=1, padx=5, pady=2)
        if item:
            desc.insert("1.0", item.description)
        row += 1

        def submit() -> None:
            try:
                _id = entries[translate(UIText.COLUMN_ID)].get().strip()
                name = entries[translate(UIText.COLUMN_NAME)].get().strip()
                price = float(entries[translate(UIText.COLUMN_PRICE)].get() or 0)
                weight = float(entries[translate(UIText.COLUMN_WEIGHT)].get() or 0)
                description = desc.get("1.0", "end").strip()
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

            new_item = SimpleItem(_id, name, price, weight, description)
            addItem(new_item)
            messagebox.showinfo(
                translate(MessageText.SAVED_TITLE),
                translate(MessageText.ITEM_SAVED),
            )
            window.destroy()

        ttk.Button(window, text=translate(UIText.SAVE_BUTTON), command=submit).grid(
            row=row, column=0, columnspan=2, pady=10
        )

    def _armor_form(self, window: tk.Toplevel, armor: Armor | None) -> None:
        self._set_icon(window)
        window.configure(bg=self.root["background"])

        entries: dict[str, tk.Entry] = {}
        row = 0
        labels = [
            UIText.COLUMN_ID,
            UIText.COLUMN_NAME,
            UIText.COLUMN_PRICE,
            UIText.COLUMN_WEIGHT,
        ]
        for label in labels:
            text = translate(label)
            ttk.Label(window, text=text).grid(
                row=row, column=0, sticky="e", padx=5, pady=2
            )
            entry = ttk.Entry(window)
            entry.grid(row=row, column=1, padx=5, pady=2)
            if armor:
                match label:
                    case UIText.COLUMN_ID:
                        entry.insert(0, armor.id)
                    case UIText.COLUMN_NAME:
                        entry.insert(0, armor.name)
                    case UIText.COLUMN_PRICE:
                        entry.insert(0, str(armor.price))
                    case UIText.COLUMN_WEIGHT:
                        entry.insert(0, str(armor.weight))
                    case _:
                        pass
            entries[text] = entry
            row += 1

        ttk.Label(window, text="AC").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        ac_entry = ttk.Entry(window, width=4)
        ac_entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        if armor:
            ac_entry.insert(0, str(armor.armorClass))
        row += 1

        dex_var = tk.BooleanVar(value=armor.dexBonus if armor else True)
        ttk.Checkbutton(window, text="Dex Bonus", variable=dex_var).grid(
            row=row, column=1, sticky="w", padx=5, pady=2
        )
        row += 1

        ttk.Label(window, text="Dex Bonus Max").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dex_max = ttk.Entry(window, width=4)
        dex_max.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        if armor and armor.dexBonusMax is not None:
            dex_max.insert(0, str(armor.dexBonusMax))
        row += 1

        ttk.Label(window, text="Strength Req").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        str_req = ttk.Entry(window, width=4)
        str_req.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        if armor and armor.strengthRequirement is not None:
            str_req.insert(0, str(armor.strengthRequirement))
        row += 1

        stealth_var = tk.BooleanVar(value=armor.stealthDisadvantage if armor else False)
        ttk.Checkbutton(window, text="Stealth Disadvantage", variable=stealth_var).grid(
            row=row, column=1, sticky="w", padx=5, pady=2
        )
        row += 1

        ttk.Label(window, text="Category").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        cat_var = tk.StringVar()
        cat_cb = ttk.Combobox(
            window,
            textvariable=cat_var,
            values=[c.value for c in ArmorCategory],
            state="readonly",
        )
        cat_cb.grid(row=row, column=1, padx=5, pady=2)
        if armor:
            cat_var.set(armor.category.value)
        else:
            cat_var.set(ArmorCategory.LIGHT.value)
        row += 1

        def submit() -> None:
            try:
                _id = entries[translate(UIText.COLUMN_ID)].get().strip()
                name = entries[translate(UIText.COLUMN_NAME)].get().strip()
                price = float(entries[translate(UIText.COLUMN_PRICE)].get() or 0)
                weight = float(entries[translate(UIText.COLUMN_WEIGHT)].get() or 0)
                ac = int(ac_entry.get() or 0)
                dex_bonus = dex_var.get()
                dex_max_val = dex_max.get()
                dex_max_i = int(dex_max_val) if dex_max_val else None
                str_req_val = str_req.get()
                str_req_i = int(str_req_val) if str_req_val else None
                stealth = stealth_var.get()
                category = to_enum(ArmorCategory, cat_var.get())
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

            new_armor = Armor(
                _id=_id,
                name=name,
                price=price,
                weight=weight,
                armorClass=ac,
                dexBonus=dex_bonus,
                dexBonusMax=dex_max_i,
                strengthRequirement=str_req_i,
                stealthDisadvantage=stealth,
                category=category,
            )
            addArmor(new_armor)
            messagebox.showinfo(
                translate(MessageText.SAVED_TITLE),
                translate(MessageText.ITEM_SAVED),
            )
            window.destroy()

        ttk.Button(window, text=translate(UIText.SAVE_BUTTON), command=submit).grid(
            row=row, column=0, columnspan=2, pady=10
        )

    def _spell_form(self, window: tk.Toplevel, spell: Spell | None) -> None:
        self._set_icon(window)
        window.configure(bg=self.root["background"])

        row = 0
        ttk.Label(window, text="ID").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        id_entry = ttk.Entry(window)
        id_entry.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            id_entry.insert(0, spell.id)
        row += 1

        ttk.Label(window, text="Name").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        name_entry = ttk.Entry(window)
        name_entry.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            name_entry.insert(0, spell.name)
        row += 1

        ttk.Label(window, text="Level").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        lvl_cb = ttk.Combobox(
            window, values=[str(i) for i in range(1, 10)], state="readonly"
        )
        lvl_cb.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            lvl_cb.set(str(spell.level))
        row += 1

        ttk.Label(window, text="Type").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        type_var = tk.StringVar()
        type_cb = ttk.Combobox(
            window,
            textvariable=type_var,
            values=[str(t) for t in SpellType],
            state="readonly",
        )
        type_cb.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            type_var.set(str(spell.type))
        row += 1

        ttk.Label(window, text="Classes").grid(
            row=row, column=0, sticky="ne", padx=5, pady=2
        )
        cls_frame = ttk.Frame(window)
        cls_frame.grid(row=row, column=1, sticky="w")
        class_vars: dict[CasterClassType, tk.BooleanVar] = {}
        for cls in CasterClassType:
            var = tk.BooleanVar(
                value=spell is not None and cls in getattr(spell, "casterClasses", [])
            )
            ttk.Checkbutton(cls_frame, text=str(cls), variable=var).pack(anchor="w")
            class_vars[cls] = var
        row += 1

        ttk.Label(window, text="Range").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        range_frame = ttk.Frame(window)
        range_frame.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        range_entry = ttk.Entry(range_frame, width=6)
        range_entry.pack(side="left")
        ttk.Label(range_frame, text="m").pack(side="left")
        if spell:
            range_entry.insert(0, str(spell.range))
        row += 1

        ttk.Label(window, text="Sub Range").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        sub_range_frame = ttk.Frame(window)
        sub_range_frame.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        sub_range_entry = ttk.Entry(sub_range_frame, width=6)
        sub_range_entry.pack(side="left")
        ttk.Label(sub_range_frame, text="m").pack(side="left")
        if spell and spell.subRange is not None:
            sub_range_entry.insert(0, str(spell.subRange))
        row += 1

        ttk.Label(window, text="Duration (s)").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dur_entry = ttk.Entry(window)
        dur_entry.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            dur_entry.insert(0, str(int(spell.duration.total_seconds())))
        row += 1

        ttk.Label(window, text="Cooldown (s)").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        cd_entry = ttk.Entry(window)
        cd_entry.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            cd_entry.insert(0, str(int(spell.cooldown.total_seconds())))
        row += 1

        ttk.Label(window, text="Casting Time").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        ct_var = tk.StringVar()
        ct_cb = ttk.Combobox(
            window,
            textvariable=ct_var,
            values=[str(c) for c in CastingTimeType],
            state="readonly",
        )
        ct_cb.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            ct_var.set(str(spell.castingTime))
        else:
            ct_var.set(str(CastingTimeType.ACTION))
        row += 1

        rit_var = tk.BooleanVar(value=spell.ritual if spell else False)
        ttk.Checkbutton(window, text="Ritual", variable=rit_var).grid(
            row=row, column=1, sticky="w", padx=5, pady=2
        )
        row += 1

        conc_var = tk.BooleanVar(value=spell.concentration if spell else False)
        ttk.Checkbutton(window, text="Concentration", variable=conc_var).grid(
            row=row, column=1, sticky="w", padx=5, pady=2
        )
        row += 1

        ttk.Label(window, text="Target").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        target_var = tk.StringVar()
        target_cb = ttk.Combobox(
            window,
            textvariable=target_var,
            values=[str(t) for t in TargetType],
            state="readonly",
        )
        target_cb.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            target_var.set(str(spell.target))
        else:
            target_var.set(str(TargetType.SELF))
        row += 1

        ttk.Label(window, text="Damage Dice Amount").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dmg_amount_entry = ttk.Entry(window, width=4)
        dmg_amount_entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        if spell and spell.damage:
            dmg_amount_entry.insert(0, str(spell.damage.diceAmount))
        row += 1

        ttk.Label(window, text="Damage Dice Type").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dmg_type_cb = ttk.Combobox(
            window, values=[str(d) for d in GAME.DICE_SIZES], state="readonly", width=4
        )
        dmg_type_cb.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        if spell and spell.damage:
            dmg_type_cb.set(str(spell.damage.diceType))
        row += 1

        ttk.Label(window, text="Damage Bonus").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dmg_bonus_entry = ttk.Entry(window, width=4)
        dmg_bonus_entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        if spell and spell.damage:
            dmg_bonus_entry.insert(0, str(spell.damage.bonus))
        row += 1

        ttk.Label(window, text="Damage Type").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        dmg_type_var = tk.StringVar()
        dmg_type_enum_cb = ttk.Combobox(
            window,
            textvariable=dmg_type_var,
            values=[str(dt) for dt in DamageType],
            state="readonly",
        )
        dmg_type_enum_cb.grid(row=row, column=1, padx=5, pady=2)
        if spell and spell.damage:
            dmg_type_var.set(str(spell.damage.damageType))
        row += 1

        ttk.Label(window, text="Components").grid(
            row=row, column=0, sticky="ne", padx=5, pady=2
        )
        comp_frame = ttk.Frame(window)
        comp_frame.grid(row=row, column=1, sticky="w")
        verbal_var = tk.BooleanVar(value=spell.components.verbal if spell else False)
        gestural_var = tk.BooleanVar(
            value=spell.components.gestural if spell else False
        )
        ttk.Checkbutton(comp_frame, text="Verbal", variable=verbal_var).pack(anchor="w")
        ttk.Checkbutton(comp_frame, text="Gestural", variable=gestural_var).pack(
            anchor="w"
        )
        mat_name = ttk.Entry(comp_frame)
        mat_cost = ttk.Entry(comp_frame, width=6)
        ttk.Label(comp_frame, text="Material").pack(anchor="w")
        mat_name.pack(anchor="w", padx=10)
        ttk.Label(comp_frame, text="Cost").pack(anchor="w")
        mat_cost.pack(anchor="w", padx=10)
        if spell and spell.components.material:
            mat_name.insert(0, spell.components.material.name)
            if spell.components.material.cost is not None:
                mat_cost.insert(0, str(spell.components.material.cost))
        row += 1

        ttk.Label(window, text="Level Bonus").grid(
            row=row, column=0, sticky="e", padx=5, pady=2
        )
        level_bonus_entry = ttk.Entry(window, width=25)
        level_bonus_entry.grid(row=row, column=1, padx=5, pady=2)
        if spell:
            level_bonus_entry.insert(0, spell.levelBonus)
        row += 1

        def submit() -> None:
            try:
                _id = id_entry.get().strip()
                name = name_entry.get().strip()
                level = int(lvl_cb.get() or 1)
                stype = to_enum(SpellType, type_var.get())
                classes = [cls for cls, var in class_vars.items() if var.get()]
                duration = timedelta(seconds=float(dur_entry.get() or 0))
                cooldown = timedelta(seconds=float(cd_entry.get() or 0))
                rng = float(range_entry.get() or 0)
                sub_rng = (
                    float(sub_range_entry.get()) if sub_range_entry.get() else None
                )
                ctime = to_enum(CastingTimeType, ct_var.get())
                target = to_enum(TargetType, target_var.get())

                dmg = None
                if dmg_amount_entry.get() or dmg_bonus_entry.get():
                    dmg = Damage(
                        int(dmg_amount_entry.get() or 0),
                        int(dmg_type_cb.get() or 1),
                        int(dmg_bonus_entry.get() or 0),
                        to_enum(
                            DamageType, dmg_type_var.get() or DamageType.SLASHING.value
                        ),
                    )
                material = None
                if mat_name.get() or mat_cost.get():
                    cost = float(mat_cost.get()) if mat_cost.get() else None
                    material = Material(mat_name.get().strip(), cost)
                comps = Components(verbal_var.get(), gestural_var.get(), material)
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

            new_spell = Spell(
                id=_id,
                name=name,
                level=level,
                type=stype,
                casterClasses=classes,
                duration=duration,
                cooldown=cooldown,
                range=rng,
                subRange=sub_rng,
                castingTime=ctime,
                ritual=rit_var.get(),
                concentration=conc_var.get(),
                target=target,
                damage=dmg,
                components=comps,
                levelBonus=level_bonus_entry.get().strip(),
            )
            addSpell(new_spell)
            messagebox.showinfo(
                translate(MessageText.SAVED_TITLE),
                translate(MessageText.ITEM_SAVED),
            )
            window.destroy()

        ttk.Button(window, text=translate(UIText.SAVE_BUTTON), command=submit).grid(
            row=row, column=0, columnspan=2, pady=10
        )

    def _open_add_weapon(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.ADD_ITEM_TITLE))
        self._item_form(window, None)

    def _open_edit_weapon(self, item: Item) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(f"{translate(UIText.EDIT_ITEM_TITLE)}: {item.name}")
        self._item_form(window, item)

    def _open_add_item(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.ADD_ITEM_TITLE))
        self._simple_item_form(window, None)

    def _open_edit_item(self, item: SimpleItem) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(f"{translate(UIText.EDIT_ITEM_TITLE)}: {item.name}")
        self._simple_item_form(window, item)

    def _open_add_armor(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.ADD_ITEM_TITLE))
        self._armor_form(window, None)

    def _open_edit_armor(self, armor: Armor) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(f"{translate(UIText.EDIT_ITEM_TITLE)}: {armor.name}")
        self._armor_form(window, armor)

    # ===== Spells =====
    def _open_add_spell(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.ADD_SPELL_TITLE))
        self._spell_form(window, None)

    def _open_edit_spell(self, spell: Spell) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(f"{translate(UIText.EDIT_SPELL_TITLE)}: {spell.name}")
        self._spell_form(window, spell)

    def _open_manage_spells(self) -> None:
        window = tk.Toplevel(self.root)
        self._set_icon(window)
        window.title(translate(UIText.MANAGE_SPELLS_TITLE))
        window.configure(bg=self.root["background"])

        spells = getSpells()

        search_var = tk.StringVar()
        ttk.Label(window, text=translate(UIText.SEARCH_LABEL)).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        search_entry = ttk.Entry(window, textvariable=search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tree = ttk.Treeview(
            window, columns=("id", "name"), show="headings", selectmode="browse"
        )
        tree.heading("id", text=translate(UIText.COLUMN_ID))
        tree.heading("name", text=translate(UIText.COLUMN_NAME))
        tree.column("id", width=100, anchor="center")
        tree.column("name", width=150, anchor="center")
        tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_VIEW_CARD),
            command=lambda: view_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_DATA),
            command=lambda: edit_selected(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame,
            text=translate(UIText.BUTTON_EDIT_CARD),
            command=lambda: print_card(),
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_CLOSE), command=window.destroy
        ).pack(side="left", padx=2)

        def filter_spells() -> List[Spell]:
            search = search_var.get().lower()
            return [
                sp
                for sp in spells
                if search in sp.id.lower() or search in sp.name.lower()
            ]

        def update_list(*_args: object) -> None:
            tree.delete(*tree.get_children())
            for sp in filter_spells():
                tree.insert("", "end", values=(sp.id, sp.name))

        def get_selected_spell() -> Spell | None:
            sel = tree.selection()
            if not sel:
                return None
            spell_id = tree.item(sel[0], "values")[0]
            for sp in spells:
                if sp.id == spell_id:
                    return sp
            return None

        def view_card() -> None:
            sp = get_selected_spell()
            if not sp:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            try:
                cache = loadSpellCache()
                t = cache.get(sp.id, {"rotate": 0.0, "scale": 1.0, "flip": False})
                self.image_handler.createSpellCard(
                    sp,
                    rotate=t.get("rotate", 0.0),
                    flip=bool(t.get("flip", False)),
                    scale=t.get("scale", 1.0),
                    offset_x=t.get("offset_x", 0.0),
                    offset_y=t.get("offset_y", 0.0),
                )
                path = join(PATHS.SPELL_OUTPUT, f"level{sp.level}", f"{sp.id}.png")
                img = Image.open(path)
                top = tk.Toplevel(window)
                self._set_icon(top)
                top.title(sp.name)
                tk_img = ImageTk.PhotoImage(img)
                lbl = ttk.Label(top, image=tk_img)
                lbl.image = tk_img  # type: ignore
                lbl.pack()
            except Exception as e:
                messagebox.showerror(
                    translate(MessageText.ERROR_TITLE),
                    str(e),
                )

        def edit_selected() -> None:
            sp = get_selected_spell()
            if not sp:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            self._open_edit_spell(sp)
            spells.clear()
            spells.extend(getSpells())
            update_list()

        def print_card() -> None:
            sp = get_selected_spell()
            if not sp:
                messagebox.showwarning(
                    translate(MessageText.NO_SELECTION_TITLE),
                    translate(MessageText.NO_SELECTION_TEXT),
                )
                return
            cache = loadSpellCache()
            SpellPreviewWindow(self.root, [sp], self.image_handler, cache)

        search_var.trace_add("write", update_list)
        update_list()

    def _open_print_spells(self) -> None:
        spells = getSpells()
        if not spells:
            messagebox.showinfo(
                translate(MessageText.NO_ITEMS_TITLE),
                translate(MessageText.NO_ITEMS_MESSAGE),
            )
            return
        cache: SpellCache = loadSpellCache()
        show_all = messagebox.askyesno(
            translate(MessageText.PREVIEW_MODE),
            translate(MessageText.PREVIEW_QUESTION),
        )
        preview_spells: List[Spell] = []
        skip_missing = get_skip_missing()
        for sp in spells:
            if show_all or sp.id not in cache:
                preview_spells.append(sp)
            else:
                t = cache[sp.id]
                try:
                    self.image_handler.createSpellCard(
                        sp,
                        rotate=t.get("rotate", 0.0),
                        flip=t.get("flip", False),
                        scale=t.get("scale", 1.0),
                        offset_x=t.get("offset_x", 0.0),
                        offset_y=t.get("offset_y", 0.0),
                    )
                except FileNotFoundError:
                    if skip_missing:
                        self.image_handler.recordMissingSpell(sp.id)
                    else:
                        raise

        if preview_spells:
            SpellPreviewWindow(self.root, preview_spells, self.image_handler, cache)
        else:
            messagebox.showinfo(
                translate(MessageText.DONE_TITLE),
                translate(MessageText.DONE_MESSAGE),
            )

    # ===== Print Weapons =====
    def _open_print_weapons(self) -> None:
        items = getWeapons()
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
        skip_missing = get_skip_missing()
        for item in items:
            if show_all or item.id not in cache:
                preview_items.append(item)
            else:
                t = cache[item.id]
                try:
                    self.image_handler.createItemCard(
                        item,
                        rotate=t.get("rotate", 0.0),
                        flip=t.get("flip", False),
                        scale=t.get("scale", 1.0),
                    )
                except FileNotFoundError:
                    if skip_missing:
                        self.image_handler.recordMissingItem(item.id)
                    else:
                        raise

        if preview_items:
            PreviewWindow(self.root, preview_items, self.image_handler, cache)
        else:
            messagebox.showinfo(
                translate(MessageText.DONE_TITLE),
                translate(MessageText.DONE_MESSAGE),
            )

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
        preview_items: List[SimpleItem] = []
        skip_missing = get_skip_missing()
        for item in items:
            if show_all or item.id not in cache:
                preview_items.append(item)
            else:
                t = cache[item.id]
                try:
                    self.image_handler.createItemCard(
                        item,
                        rotate=t.get("rotate", 0.0),
                        flip=t.get("flip", False),
                        scale=t.get("scale", 1.0),
                    )
                except FileNotFoundError:
                    if skip_missing:
                        self.image_handler.recordMissingItem(item.id)
                    else:
                        raise

        if preview_items:
            PreviewWindow(self.root, preview_items, self.image_handler, cache)
        else:
            messagebox.showinfo(
                translate(MessageText.DONE_TITLE),
                translate(MessageText.DONE_MESSAGE),
            )

    def _open_print_armors(self) -> None:
        items = getArmors()
        if not items:
            messagebox.showinfo(
                translate(MessageText.NO_ITEMS_TITLE),
                translate(MessageText.NO_ITEMS_MESSAGE),
            )
            return

        cache: ItemCache = loadItemCache()
        show_all = messagebox.askyesno(
            translate(MessageText.PREVIEW_MODE),
            translate(MessageText.PREVIEW_QUESTION),
        )
        preview_items: List[Armor] = []
        skip_missing = get_skip_missing()
        for item in items:
            if show_all or item.id not in cache:
                preview_items.append(item)
            else:
                t = cache[item.id]
                try:
                    self.image_handler.createItemCard(
                        item,
                        rotate=t.get("rotate", 0.0),
                        flip=t.get("flip", False),
                        scale=t.get("scale", 1.0),
                    )
                except FileNotFoundError:
                    if skip_missing:
                        self.image_handler.recordMissingItem(item.id)
                    else:
                        raise

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
        items: Sequence[Union[Item, SimpleItem, Armor]],
        image_handler: ImageHandler,
        cache: ItemCache,
    ) -> None:
        super().__init__(root)
        try:
            icon = tk.PhotoImage(file=IMAGE.PATHS.APP_ICON)
            self.iconphoto(True, icon)
        except Exception:
            pass
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
        ttk.Scale(
            btn_frame,
            from_=-180,
            to=180,
            orient="horizontal",
            variable=self.angle_var,
            command=self._update_angle,
            length=150,
        ).pack(side="left", padx=2)
        self.scale_var = tk.DoubleVar(value=1.0)
        ttk.Scale(
            btn_frame,
            from_=0.5,
            to=1.5,
            orient="horizontal",
            variable=self.scale_var,
            command=self._update_scale,
            length=150,
        ).pack(side="left", padx=2)
        self.x_var = tk.DoubleVar(value=0)
        ttk.Scale(
            btn_frame,
            from_=-50,
            to=50,
            orient="horizontal",
            variable=self.x_var,
            command=self._update_offset,
            length=100,
        ).pack(side="left", padx=2)
        self.y_var = tk.DoubleVar(value=0)
        ttk.Scale(
            btn_frame,
            from_=-50,
            to=50,
            orient="horizontal",
            variable=self.y_var,
            command=self._update_offset,
            length=100,
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_FLIP), command=self._toggle_flip
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_SKIP), command=self._skip
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_NEXT), command=self._next
        ).pack(side="left", padx=2)
        self.flip: bool = False
        self.skip_flag = False

        self.original: Image.Image | None = None
        self.display: Image.Image | None = None
        self.tk_img: ImageTk.PhotoImage | None = None
        self._load_current()

    def _load_current(self) -> None:
        item = self.items[self.index]
        t = self.cache.get(item.id, {"rotate": 0.0, "scale": 1.0, "flip": False})
        self.angle_var.set(float(t.get("rotate", 0.0)))
        self.scale_var.set(float(t.get("scale", 1.0)))
        self.flip = bool(t.get("flip", False))
        self.x_var.set(float(t.get("offset_x", 0.0)))
        self.y_var.set(float(t.get("offset_y", 0.0)))
        if not self._generate_image(item):
            return
        self._update_image()

    def _generate_image(self, item: Union[Item, SimpleItem, Armor]) -> bool:
        try:
            self.image_handler.createItemCard(
                item,
                rotate=self.angle_var.get(),
                flip=self.flip,
                scale=self.scale_var.get(),
                offset_x=self.x_var.get(),
                offset_y=self.y_var.get(),
            )
        except FileNotFoundError:
            if get_skip_missing():
                self.image_handler.recordMissingItem(item.id)
                self.skip_flag = True
                return False
            if messagebox.askretrycancel(
                translate(MessageText.MISSING_IMAGE_TITLE),
                translate(MessageText.MISSING_IMAGE_MESSAGE).format(id=item.id),
            ):
                return self._generate_image(item)
            else:
                self.skip_flag = True
                return False
        path = self.image_handler.getItemOutputPath(item)
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

    def _update_offset(self, _value: str) -> None:
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
                self.x_var.get(),
                self.y_var.get(),
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


class SpellPreviewWindow(tk.Toplevel):
    def __init__(
        self,
        root: tk.Tk,
        spells: List[Spell],
        image_handler: ImageHandler,
        cache: SpellCache,
    ) -> None:
        super().__init__(root)
        try:
            icon = tk.PhotoImage(file=IMAGE.PATHS.APP_ICON)
            self.iconphoto(True, icon)
        except Exception:
            pass
        self.title(translate(UIText.SPELL_PREVIEW_TITLE))
        self.configure(bg=root["background"])
        self.spells = spells
        self.index = 0
        self.image_handler = image_handler
        self.cache = cache
        self.skipped: set[str] = set()
        self.label = ttk.Label(self)
        self.label.pack(padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack()
        self.angle_var = tk.DoubleVar(value=0)
        ttk.Scale(
            btn_frame,
            from_=-180,
            to=180,
            orient="horizontal",
            variable=self.angle_var,
            command=self._update_angle,
            length=150,
        ).pack(side="left", padx=2)
        self.scale_var = tk.DoubleVar(value=1.0)
        ttk.Scale(
            btn_frame,
            from_=0.5,
            to=1.5,
            orient="horizontal",
            variable=self.scale_var,
            command=self._update_scale,
            length=150,
        ).pack(side="left", padx=2)
        self.x_var = tk.DoubleVar(value=0)
        ttk.Scale(
            btn_frame,
            from_=-50,
            to=50,
            orient="horizontal",
            variable=self.x_var,
            command=self._update_offset,
            length=100,
        ).pack(side="left", padx=2)
        self.y_var = tk.DoubleVar(value=0)
        ttk.Scale(
            btn_frame,
            from_=-50,
            to=50,
            orient="horizontal",
            variable=self.y_var,
            command=self._update_offset,
            length=100,
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_FLIP), command=self._toggle_flip
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_SKIP), command=self._skip
        ).pack(side="left", padx=2)
        ttk.Button(
            btn_frame, text=translate(UIText.BUTTON_NEXT), command=self._next
        ).pack(side="left", padx=2)
        self.flip: bool = False
        self.skip_flag = False

        self.original: Image.Image | None = None
        self.display: Image.Image | None = None
        self.tk_img: ImageTk.PhotoImage | None = None
        self._load_current()

    def _load_current(self) -> None:
        sp = self.spells[self.index]
        t = self.cache.get(sp.id, {"rotate": 0.0, "scale": 1.0, "flip": False})
        self.angle_var.set(float(t.get("rotate", 0.0)))
        self.scale_var.set(float(t.get("scale", 1.0)))
        self.flip = bool(t.get("flip", False))
        self.x_var.set(float(t.get("offset_x", 0.0)))
        self.y_var.set(float(t.get("offset_y", 0.0)))
        if not self._generate_image(sp):
            return
        self._update_image()

    def _generate_image(self, spell: Spell) -> bool:
        try:
            self.image_handler.createSpellCard(
                spell,
                rotate=self.angle_var.get(),
                flip=self.flip,
                scale=self.scale_var.get(),
                offset_x=self.x_var.get(),
                offset_y=self.y_var.get(),
            )
        except FileNotFoundError:
            if get_skip_missing():
                self.image_handler.recordMissingSpell(spell.id)
                self.skip_flag = True
                return False
            if messagebox.askretrycancel(
                translate(MessageText.MISSING_IMAGE_TITLE),
                translate(MessageText.MISSING_IMAGE_MESSAGE).format(id=spell.id),
            ):
                return self._generate_image(spell)
            else:
                self.skip_flag = True
                return False
        level_dir = join(PATHS.SPELL_OUTPUT, f"level{spell.level}")
        path = join(level_dir, f"{spell.id}.png")
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

    def _update_offset(self, _value: str) -> None:
        self._apply_transform()

    def _toggle_flip(self) -> None:
        self.flip = not self.flip
        self._apply_transform()

    def _apply_transform(self) -> None:
        sp = self.spells[self.index]
        if not self._generate_image(sp):
            return
        self._update_image()

    def _next(self) -> None:
        sp = self.spells[self.index]
        if not self.skip_flag:
            updateSpellCache(
                sp.id,
                self.angle_var.get(),
                self.scale_var.get(),
                self.flip,
                self.x_var.get(),
                self.y_var.get(),
            )
        self.skip_flag = False
        self.index += 1
        if self.index >= len(self.spells):
            self.destroy()
            return
        self._load_current()

    def _skip(self) -> None:
        self.skip_flag = True
        self._next()
