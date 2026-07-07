# -*- coding: utf-8 -*-
"""
app.py — Кроссплатформенный GUI для генератора паролей (Tkinter).
Автоматически подбирает шрифт с кириллицей.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_password
from settings import load_services, save_services, load_settings, save_settings


# ── Подбор шрифта с кириллицей ─────────────────────────────────
FONT_CANDIDATES = [
    ("Liberation Sans", 11),     # Linux (ttf-liberation)
    ("DejaVu Sans", 11),         # Linux (ttf-dejavu)
    ("Noto Sans", 11),           # Linux (noto-fonts)
]

MONO_CANDIDATES = [
    "Liberation Mono",
    "DejaVu Sans Mono",
    "Noto Sans Mono",
    "Courier New",
    "Courier",
]

TEST_STRING = "СидСервисДлинаСимволыCopyABCDabcd1234"


def _font_exists(family, size):
    """Проверить, установлен ли шрифт (не fallback-замена)."""
    try:
        f = font.Font(family=family, size=size)
        # actual("family") возвращает системное имя — если оно совпадает
        # с запрошенным, значит шрифт реально установлен
        return f.actual("family") == family
    except Exception:
        return False


def _pick_fonts():
    """Выбрать лучший доступный шрифт (основной и моноширинный)."""
    base = ("TkDefaultFont", 11)
    for family, size in FONT_CANDIDATES:
        if _font_exists(family, size):
            base = (family, size)
            break

    mono = ("TkFixedFont", 12)
    for family in MONO_CANDIDATES:
        if _font_exists(family, 12):
            mono = (family, 12)
            break

    return base, mono


# ── Цвета ──────────────────────────────────────────────────────
BG        = "#f8f8ff"
FG        = "#1a1a1a"
BTN_LILAC = "#a855f7"
BTN_HVR   = "#c084fc"
BTN_EDGE  = "#7c3aed"
BTN_VIOLET= "#a78bfa"
ENTRY_BG  = "#ffffff"
MUTED     = "#888888"


class PassGenApp(tk.Tk):
    """Главное окно."""

    def __init__(self):
        super().__init__()
        self.title("passgen")
        self.configure(bg=BG)

        win_w, win_h = 380, 460
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{win_w}x{win_h}+{(sw-win_w)//2}+{(sh-win_h)//2}")
        self.resizable(False, False)

        # Подбор шрифтов
        self._base_font, self._mono_font = _pick_fonts()

        self._build_ui()
        self._load_data()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Построение интерфейса ───────────────────────────────────

    def _build_ui(self):
        self.configure(bg=BG)

        FONT_REG    = self._base_font
        FONT_BOLD   = (self._base_font[0], self._base_font[1], "bold")
        FONT_TITLE  = (self._base_font[0], 16, "bold")
        FONT_PWD    = (self._mono_font[0], self._mono_font[1], "bold")
        FONT_SMALL  = (self._base_font[0], 9)

        # Заголовок
        self._make_title("passgen  -  Password Generator", FONT_TITLE)

        # Сид-фраза
        self._make_label("Master seed:", FONT_REG)
        self.seed_var = tk.StringVar()
        self.seed_entry = self._make_entry(self.seed_var, FONT_REG)
        self.seed_entry.pack(fill="x", padx=28, pady=(0, 10), ipady=4)

        # Сервис
        self._make_label("Service:", FONT_REG)
        self.svc_var = tk.StringVar()
        self.svc_combo = ttk.Combobox(self, textvariable=self.svc_var,
                                       font=FONT_REG)
        self.svc_combo.pack(fill="x", padx=28, pady=(0, 10))
        self.svc_combo.bind("<Return>", lambda e: self._generate())
        self.svc_combo.bind("<KP_Enter>", lambda e: self._generate())

        # Длина
        frame_len = tk.Frame(self, bg=BG)
        frame_len.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_len, text="Length:", font=FONT_REG,
                 bg=BG, fg=FG).pack(side="left")
        self.len_var = tk.IntVar(value=10)
        self.len_spin = tk.Spinbox(frame_len, from_=1, to=99,
                                    textvariable=self.len_var,
                                    font=FONT_REG, width=6,
                                    relief="sunken", bd=2,
                                    bg=ENTRY_BG, fg=FG)
        self.len_spin.pack(side="right")

        # Чекбоксы
        frame_chk = tk.Frame(self, bg=BG)
        frame_chk.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_chk, text="Charset:", font=FONT_REG,
                 bg=BG, fg=FG).grid(row=0, column=0, sticky="nw",
                                    padx=(0, 18), pady=(2, 0))

        self.cap_var = tk.BooleanVar(value=True)
        self.low_var = tk.BooleanVar(value=True)
        self.dig_var = tk.BooleanVar(value=False)
        self.sym_var = tk.BooleanVar(value=True)

        chk_frame = tk.Frame(frame_chk, bg=BG)
        chk_frame.grid(row=0, column=1, sticky="w")

        self._make_chk(chk_frame, "Capitals",   self.cap_var, 0, 0, FONT_REG)
        self._make_chk(chk_frame, "Lowercase",     self.low_var, 0, 1, FONT_REG)
        self._make_chk(chk_frame, "Digits",        self.dig_var, 1, 0, FONT_REG)
        self._make_chk(chk_frame, "Symbols",  self.sym_var, 1, 1, FONT_REG)

        # Кнопка генерации
        self.gen_btn = self._make_btn("Generate", FONT_BOLD,
                                      BTN_LILAC, self._generate)
        self.gen_btn.pack(fill="x", padx=28, pady=(4, 10), ipady=6)

        # Поле пароля
        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(self, textvariable=self.pwd_var,
                                   font=FONT_PWD,
                                   relief="sunken", bd=2,
                                   bg=ENTRY_BG, fg=FG,
                                   state="readonly")
        self.pwd_entry.pack(fill="x", padx=28, pady=(0, 6), ipady=6)

        # Индикатор надёжности
        self.strength_var = tk.StringVar()
        tk.Label(self, textvariable=self.strength_var,
                 font=FONT_SMALL, bg=BG, fg=MUTED
        ).pack(anchor="w", padx=28, pady=(0, 6))

        # Кнопка копирования
        self.copy_btn = self._make_btn("Copy", FONT_BOLD,
                                       BTN_VIOLET, self._copy_password)
        self.copy_btn.pack(fill="x", padx=28, pady=(0, 24), ipady=6)

    # ── Вспомогательные методы ──────────────────────────────────

    def _make_title(self, text, font):
        tk.Label(self, text=text, font=font, bg=BG, fg="#4a1a6b"
        ).pack(anchor="w", padx=28, pady=(22, 18))

    def _make_label(self, text, font):
        tk.Label(self, text=text, font=font, bg=BG, fg=FG
        ).pack(anchor="w", padx=28)

    def _make_entry(self, var, font):
        return tk.Entry(self, textvariable=var, font=font,
                         relief="sunken", bd=2,
                         bg=ENTRY_BG, fg=FG)

    def _make_chk(self, parent, text, var, row, col, font):
        cb = tk.Checkbutton(parent, text=text, variable=var,
                             font=font, bg=BG, fg=FG,
                             selectcolor=ENTRY_BG,
                             activebackground=BG, relief="flat")
        cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=2)

    def _make_btn(self, text, font, color, command):
        btn = tk.Button(self, text=text, command=command,
                         font=font,
                         bg=color, fg="#ffffff",
                         activebackground=BTN_HVR,
                         activeforeground="#ffffff",
                         relief="raised", bd=3,
                         highlightbackground=BTN_EDGE,
                         cursor="hand2")
        return btn

    # ── Загрузка / сохранение ───────────────────────────────────

    def _load_data(self):
        s = load_settings()
        self.len_var.set(s["length"])
        self.cap_var.set(s["capitals"])
        self.low_var.set(s["lower"])
        self.dig_var.set(s["digits"])
        self.sym_var.set(s["symbols"])

        svcs = load_services()
        if svcs:
            self.svc_combo["values"] = svcs

    def _save_data(self):
        save_settings(
            length=self.len_var.get(),
            capitals=self.cap_var.get(),
            lower=self.low_var.get(),
            digits=self.dig_var.get(),
            symbols=self.sym_var.get(),
        )
        services = list(self.svc_combo["values"])
        cur = self.svc_var.get().strip()
        if cur and cur not in services:
            services.append(cur)
        save_services(services)

    # ── Логика ──────────────────────────────────────────────────

    def _generate(self):
        service = self.svc_var.get().strip()
        seed = self.seed_var.get().strip()

        if not seed:
            messagebox.showwarning("", "Enter master seed")
            return
        if not service:
            messagebox.showwarning("", "Enter service name")
            return

        try:
            pwd = generate_password(
                master_seed=seed, service=service,
                length=self.len_var.get(),
                use_capitals=self.cap_var.get(),
                use_lower=self.low_var.get(),
                use_digits=self.dig_var.get(),
                use_symbols=self.sym_var.get(),
            )
            self.pwd_var.set(pwd)

            vals = list(self.svc_combo["values"])
            if service not in vals:
                vals.append(service)
                self.svc_combo["values"] = vals

        except ValueError as ex:
            messagebox.showwarning("", str(ex))

    def _copy_password(self):
        pwd = self.pwd_var.get()
        if not pwd:
            return
        self.clipboard_clear()
        self.clipboard_append(pwd)

        old = self.copy_btn["text"]
        self.copy_btn.config(text="[ Copied ]")
        self.after(1500, lambda: self.copy_btn.config(text=old))

    def _on_close(self):
        self._save_data()
        self.destroy()


if __name__ == "__main__":
    app = PassGenApp()
    app.mainloop()
