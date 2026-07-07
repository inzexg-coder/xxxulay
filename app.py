"""
app.py — Кроссплатформенный GUI для генератора паролей (Tkinter/ttk).

Запуск:
    python app.py

Работает на Windows, Linux (Arch), macOS без дополнительных зависимостей.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_password
from settings import load_services, save_services, load_settings, save_settings


# ── Цветовая схема ──────────────────────────────────────────────
COLORS = {
    "bg": "#1e1e2e",          # тёмный фон
    "fg": "#cdd6f4",          # светлый текст
    "accent": "#89b4fa",      # акцент (синий)
    "surface": "#313244",     # карточки / поля
    "border": "#45475a",      # рамки
    "success": "#a6e3a1",     # зелёный
    "error": "#f38ba8",       # красный
    "text_muted": "#6c7086",  # приглушённый
}


class PassGenApp(tk.Tk):
    """Главное окно генератора паролей."""

    def __init__(self):
        super().__init__()
        self.title("passgen")
        self.configure(bg=COLORS["bg"])

        # Размер и центрирование
        win_w, win_h = 340, 420
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - win_w) // 2
        y = (sh - win_h) // 2
        self.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.resizable(False, False)

        # Настройка стилей ttk
        self._setup_styles()

        # Сборка интерфейса
        self._build_ui()

        # Загрузка данных
        self._load_data()

        # Привязка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Стилизация ──────────────────────────────────────────────

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TLabel",
                        background=COLORS["bg"],
                        foreground=COLORS["fg"],
                        font=("Segoe UI", 10))

        style.configure("TEntry",
                        fieldbackground=COLORS["surface"],
                        foreground=COLORS["fg"],
                        bordercolor=COLORS["border"],
                        lightcolor=COLORS["border"],
                        darkcolor=COLORS["border"],
                        font=("Segoe UI", 10))

        style.configure("TCombobox",
                        fieldbackground=COLORS["surface"],
                        foreground=COLORS["fg"],
                        bordercolor=COLORS["border"],
                        arrowcolor=COLORS["fg"],
                        font=("Segoe UI", 10))
        style.map("TCombobox",
                  fieldbackground=[("readonly", COLORS["surface"])])

        style.configure("TCheckbutton",
                        background=COLORS["bg"],
                        foreground=COLORS["fg"],
                        font=("Segoe UI", 10))
        style.map("TCheckbutton",
                  background=[("active", COLORS["bg"])])

        style.configure("TButton",
                        background=COLORS["accent"],
                        foreground=COLORS["bg"],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0,
                        focusthickness=0)
        style.map("TButton",
                  background=[("active", "#74c7ec"), ("pressed", "#89b4fa")])

        style.configure("Success.TButton",
                        background=COLORS["success"],
                        foreground=COLORS["bg"],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0,
                        focusthickness=0)
        style.map("Success.TButton",
                  background=[("active", "#94eb9c"), ("pressed", "#a6e3a1")])

        style.configure("Muted.TLabel",
                        background=COLORS["bg"],
                        foreground=COLORS["text_muted"],
                        font=("Segoe UI", 8))

        style.configure("Title.TLabel",
                        background=COLORS["bg"],
                        foreground=COLORS["fg"],
                        font=("Segoe UI", 12, "bold"))

        style.configure("Result.TEntry",
                        fieldbackground=COLORS["surface"],
                        foreground=COLORS["success"],
                        bordercolor=COLORS["border"],
                        font=("Consolas", 11, "bold"))

    # ── Построение UI ───────────────────────────────────────────

    def _build_ui(self):
# Отступы
        pad = {"padx": 20, "pady": (0, 4)}
        pass  #
        pass  #

        # ── Заголовок ──
        title = ttk.Label(self, text="🔐 passgen", style="Title.TLabel")
        title.pack(anchor="w", padx=20, pady=(20, 16))

        # ── Сид-фраза ──
        row_seed = tk.Frame(self, bg=COLORS["bg"])
        row_seed.pack(fill="x", padx=20, pady=(0, 8))

        ttk.Label(row_seed, text="Сид-фраза:").pack(side="left")
        self.seed_var = tk.StringVar()
        self.seed_entry = ttk.Entry(row_seed, textvariable=self.seed_var, width=22)
        self.seed_entry.pack(side="right")

        # ── Сервис ──
        row_svc = tk.Frame(self, bg=COLORS["bg"])
        row_svc.pack(fill="x", padx=20, pady=(0, 8))

        ttk.Label(row_svc, text="Сервис:").pack(side="left")
        self.svc_var = tk.StringVar()
        self.svc_combo = ttk.Combobox(row_svc, textvariable=self.svc_var, width=20)
        self.svc_combo.pack(side="right")
        self.svc_combo.bind("<Return>", lambda e: self._generate())
        self.svc_combo.bind("<KP_Enter>", lambda e: self._generate())

        # ── Длина ──
        row_len = tk.Frame(self, bg=COLORS["bg"])
        row_len.pack(fill="x", padx=20, pady=(0, 8))

        ttk.Label(row_len, text="Длина:").pack(side="left")
        self.len_var = tk.IntVar(value=10)
        self.len_spin = tk.Spinbox(
            row_len, from_=1, to=99, textvariable=self.len_var,
            width=5, font=("Segoe UI", 10),
            bg=COLORS["surface"], fg=COLORS["fg"],
            buttonbackground=COLORS["bg"],
            relief="flat", bd=0,
        )
        self.len_spin.pack(side="right")

        # ── Чекбоксы ──
        row_chk = tk.Frame(self, bg=COLORS["bg"])
        row_chk.pack(fill="x", padx=20, pady=(0, 8))
        ttk.Label(row_chk, text="Символы:").pack(anchor="nw", pady=(4, 0))

        chk_frame = tk.Frame(row_chk, bg=COLORS["bg"])
        chk_frame.pack(fill="x", pady=(4, 0))

        self.cap_var = tk.BooleanVar(value=True)
        self.low_var = tk.BooleanVar(value=True)
        self.dig_var = tk.BooleanVar(value=False)
        self.sym_var = tk.BooleanVar(value=True)

        chk_cap = ttk.Checkbutton(chk_frame, text="Заглавные",
                                  variable=self.cap_var)
        chk_cap.grid(row=0, column=0, sticky="w", padx=(0, 12))

        chk_low = ttk.Checkbutton(chk_frame, text="Строчные",
                                  variable=self.low_var)
        chk_low.grid(row=0, column=1, sticky="w", padx=(0, 12))

        chk_dig = ttk.Checkbutton(chk_frame, text="Цифры",
                                  variable=self.dig_var)
        chk_dig.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=(4, 0))

        chk_sym = ttk.Checkbutton(chk_frame, text="Спецсимволы",
                                  variable=self.sym_var)
        chk_sym.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(4, 0))

        # ── Кнопка генерации ──
        self.gen_btn = ttk.Button(self, text="Готово",
                                  style="TButton",
                                  command=self._generate)
        self.gen_btn.pack(fill="x", padx=20, pady=(4, 8))

        # ── Поле пароля ──
        self.pwd_var = tk.StringVar()
        self.pwd_entry = ttk.Entry(self, textvariable=self.pwd_var,
                                   style="Result.TEntry",
                                   state="readonly")
        self.pwd_entry.pack(fill="x", padx=20, pady=(0, 4))

        # ── Индикатор надёжности (заглушка, будет позже) ──
        self.strength_label = ttk.Label(self, text="",
                                        style="Muted.TLabel")
        self.strength_label.pack(anchor="w", padx=(20, 0), pady=(0, 4))

        # ── Кнопка копирования ──
        self.copy_btn = ttk.Button(self, text="Скопировать",
                                   style="Success.TButton",
                                   command=self._copy_password)
        self.copy_btn.pack(fill="x", padx=20, pady=(0, 20))

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
        # Собираем историю сервисов
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

            # Обновить список сервисов
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

        # Визуальный фидбек
        old_text = self.copy_btn["text"]
        self.copy_btn.config(text="✓ Скопировано")
        self.after(1500, lambda: self.copy_btn.config(text=old_text))

    def _on_close(self):
        self._save_data()
        self.destroy()


if __name__ == "__main__":
    app = PassGenApp()
    app.mainloop()
