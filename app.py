# -*- coding: utf-8 -*-
"""
app.py — Кроссплатформенный GUI для генератора паролей (Tkinter).
Светлый дизайн, сиреневые кнопки с эффектом тиснения.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_password
from settings import load_services, save_services, load_settings, save_settings


# ── Шрифты (гарантированно есть на Arch, Windows, macOS) ───────
FONT_REG  = ("Liberation Sans", 11)
FONT_BOLD = ("Liberation Sans", 11, "bold")
FONT_TITLE= ("Liberation Sans", 16, "bold")
FONT_PWD  = ("Liberation Mono", 12, "bold")
FONT_SMALL= ("Liberation Sans", 9)

# ── Цвета ──────────────────────────────────────────────────────
BG       = "#f8f8ff"
FG       = "#1a1a1a"
BTN_LILAC= "#a855f7"
BTN_HVR  = "#c084fc"
BTN_EDGE = "#7c3aed"
BTN_VIO  = "#a78bfa"
ENTRY_BG = "#ffffff"
MUTED    = "#888888"


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

        self._build_ui()
        self._load_data()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Построение интерфейса ───────────────────────────────────

    def _build_ui(self):
        self.configure(bg=BG)

        # Заголовок
        tk.Label(self, text="passgen  |  Password Generator",
                 font=FONT_TITLE, bg=BG, fg="#4a1a6b"
        ).pack(anchor="w", padx=28, pady=(22, 18))

        # ── Сид-фраза ───────────────────────────────────────────
        self._label("Сид-фраза:")
        self.seed_var = tk.StringVar()
        self.seed_entry = tk.Entry(self, textvariable=self.seed_var,
                                    font=FONT_REG, relief="sunken", bd=2,
                                    bg=ENTRY_BG, fg=FG)
        self.seed_entry.pack(fill="x", padx=28, pady=(0, 10), ipady=4)

        # ── Сервис ──────────────────────────────────────────────
        self._label("Сервис:")
        self.svc_var = tk.StringVar()
        self.svc_combo = ttk.Combobox(self, textvariable=self.svc_var,
                                       font=FONT_REG)
        self.svc_combo.pack(fill="x", padx=28, pady=(0, 10))
        self.svc_combo.bind("<Return>", lambda e: self._generate())
        self.svc_combo.bind("<KP_Enter>", lambda e: self._generate())

        # ── Длина ───────────────────────────────────────────────
        frame_len = tk.Frame(self, bg=BG)
        frame_len.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_len, text="Длина:", font=FONT_REG,
                 bg=BG, fg=FG).pack(side="left")
        self.len_var = tk.IntVar(value=10)
        self.len_spin = tk.Spinbox(frame_len, from_=1, to=99,
                                    textvariable=self.len_var,
                                    font=FONT_REG, width=6,
                                    relief="sunken", bd=2,
                                    bg=ENTRY_BG, fg=FG)
        self.len_spin.pack(side="right")

        # ── Чекбоксы ────────────────────────────────────────────
        frame_chk = tk.Frame(self, bg=BG)
        frame_chk.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_chk, text="Символы:", font=FONT_REG,
                 bg=BG, fg=FG).grid(row=0, column=0, sticky="nw",
                                    padx=(0, 18), pady=(2, 0))

        self.cap_var = tk.BooleanVar(value=True)
        self.low_var = tk.BooleanVar(value=True)
        self.dig_var = tk.BooleanVar(value=False)
        self.sym_var = tk.BooleanVar(value=True)

        chk_frame = tk.Frame(frame_chk, bg=BG)
        chk_frame.grid(row=0, column=1, sticky="w")

        self._chk(chk_frame, "Заглавные",   self.cap_var, 0, 0)
        self._chk(chk_frame, "Строчные",     self.low_var, 0, 1)
        self._chk(chk_frame, "Цифры",        self.dig_var, 1, 0)
        self._chk(chk_frame, "Спецсимволы",  self.sym_var, 1, 1)

        # ── Кнопка генерации ────────────────────────────────────
        self.gen_btn = self._btn("Сгенерировать", BTN_LILAC, self._generate)
        self.gen_btn.pack(fill="x", padx=28, pady=(4, 10), ipady=6)

        # ── Поле пароля ─────────────────────────────────────────
        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(self, textvariable=self.pwd_var,
                                   font=FONT_PWD,
                                   relief="sunken", bd=2,
                                   bg=ENTRY_BG, fg=FG,
                                   state="readonly")
        self.pwd_entry.pack(fill="x", padx=28, pady=(0, 6), ipady=6)

        # ── Индикатор надёжности ────────────────────────────────
        self.strength_var = tk.StringVar()
        tk.Label(self, textvariable=self.strength_var,
                 font=FONT_SMALL, bg=BG, fg=MUTED
        ).pack(anchor="w", padx=28, pady=(0, 6))

        # ── Кнопка копирования ──────────────────────────────────
        self.copy_btn = self._btn("Скопировать", BTN_VIO, self._copy_password)
        self.copy_btn.pack(fill="x", padx=28, pady=(0, 24), ipady=6)

    # ── Вспомогательные виджеты ─────────────────────────────────

    def _label(self, text):
        tk.Label(self, text=text, font=FONT_REG, bg=BG, fg=FG
        ).pack(anchor="w", padx=28)

    def _chk(self, parent, text, var, row, col):
        cb = tk.Checkbutton(parent, text=text, variable=var,
                             font=FONT_REG, bg=BG, fg=FG,
                             selectcolor=ENTRY_BG,
                             activebackground=BG, relief="flat")
        cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=2)

    def _btn(self, text, color, command):
        btn = tk.Button(self, text=text, command=command,
                         font=FONT_BOLD,
                         bg=color, fg="#ffffff",
                         activebackground=BTN_HVR,
                         activeforeground="#ffffff",
                         relief="raised", bd=3,
                         highlightbackground=BTN_EDGE,
                         cursor="hand2")
        return btn

    # ── Загрузка / сохранение ───────────────────────────────────

    def _load_data(self):
        settings = load_settings()
        self.len_var.set(settings["length"])
        self.cap_var.set(settings["capitals"])
        self.low_var.set(settings["lower"])
        self.dig_var.set(settings["digits"])
        self.sym_var.set(settings["symbols"])

        services = load_services()
        if services:
            self.svc_combo["values"] = services

    def _save_data(self):
        save_settings(
            length=self.len_var.get(),
            capitals=self.cap_var.get(),
            lower=self.low_var.get(),
            digits=self.dig_var.get(),
            symbols=self.sym_var.get(),
        )
        services = list(self.svc_combo["values"])
        current = self.svc_var.get().strip()
        if current and current not in services:
            services.append(current)
        save_services(services)

    # ── Логика ──────────────────────────────────────────────────

    def _generate(self):
        service = self.svc_var.get().strip()
        master_seed = self.seed_var.get().strip()

        if not master_seed:
            messagebox.showwarning("Ошибка", "Введите сид-фразу")
            return
        if not service:
            messagebox.showwarning("Ошибка", "Введите название сервиса")
            return

        try:
            password = generate_password(
                master_seed=master_seed,
                service=service,
                length=self.len_var.get(),
                use_capitals=self.cap_var.get(),
                use_lower=self.low_var.get(),
                use_digits=self.dig_var.get(),
                use_symbols=self.sym_var.get(),
            )
            self.pwd_var.set(password)

            values = list(self.svc_combo["values"])
            if service not in values:
                values.append(service)
                self.svc_combo["values"] = values

        except ValueError as ex:
            messagebox.showwarning("Ошибка", str(ex))

    def _copy_password(self):
        pwd = self.pwd_var.get()
        if not pwd:
            return
        self.clipboard_clear()
        self.clipboard_append(pwd)

        old = self.copy_btn["text"]
        self.copy_btn.config(text="[ Скопировано ]")
        self.after(1500, lambda: self.copy_btn.config(text=old))

    def _on_close(self):
        self._save_data()
        self.destroy()


if __name__ == "__main__":
    app = PassGenApp()
    app.mainloop()
