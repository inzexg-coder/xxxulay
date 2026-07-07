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


class PassGenApp(tk.Tk):
    """Главное окно."""

    def __init__(self):
        super().__init__()
        self.title("passgen")
        self.configure(bg="#f8f8ff")

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
        bg = "#f8f8ff"
        font_label = ("Helvetica", 11)
        font_entry = ("Helvetica", 11)
        font_pwd   = ("Courier", 12, "bold")

        self.configure(bg=bg)

        # Заголовок
        tk.Label(self, text="🔐 passgen",
                 font=("Helvetica", 16, "bold"),
                 bg=bg, fg="#4a1a6b").pack(anchor="w", padx=28, pady=(22, 18))

        # ── Сид-фраза ───────────────────────────────────────────
        self._row_label("Сид-фраза:", padx=28)
        self.seed_var = tk.StringVar()
        self.seed_entry = tk.Entry(self, textvariable=self.seed_var,
                                    font=font_entry, relief="sunken", bd=2,
                                    bg="#ffffff", fg="#1a1a1a")
        self.seed_entry.pack(fill="x", padx=28, pady=(0, 10), ipady=4)

        # ── Сервис ──────────────────────────────────────────────
        self._row_label("Сервис:", padx=28)
        self.svc_var = tk.StringVar()
        self.svc_combo = ttk.Combobox(self, textvariable=self.svc_var,
                                       font=font_entry)
        self.svc_combo.pack(fill="x", padx=28, pady=(0, 10))
        self.svc_combo.bind("<Return>", lambda e: self._generate())
        self.svc_combo.bind("<KP_Enter>", lambda e: self._generate())

        # ── Длина ───────────────────────────────────────────────
        frame_len = tk.Frame(self, bg=bg)
        frame_len.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_len, text="Длина:", font=font_label,
                 bg=bg, fg="#1a1a1a").pack(side="left")
        self.len_var = tk.IntVar(value=10)
        self.len_spin = tk.Spinbox(frame_len, from_=1, to=99,
                                    textvariable=self.len_var,
                                    font=font_entry, width=6,
                                    relief="sunken", bd=2,
                                    bg="#ffffff", fg="#1a1a1a")
        self.len_spin.pack(side="right")

        # ── Чекбоксы ────────────────────────────────────────────
        frame_chk = tk.Frame(self, bg=bg)
        frame_chk.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_chk, text="Символы:", font=font_label,
                 bg=bg, fg="#1a1a1a").grid(row=0, column=0, sticky="nw",
                                           padx=(0, 18), pady=(2, 0))

        chk_bg = bg
        self.cap_var = tk.BooleanVar(value=True)
        self.low_var = tk.BooleanVar(value=True)
        self.dig_var = tk.BooleanVar(value=False)
        self.sym_var = tk.BooleanVar(value=True)

        chk_frame = tk.Frame(frame_chk, bg=bg)
        chk_frame.grid(row=0, column=1, sticky="w")

        self._make_chk(chk_frame, "Заглавные",   self.cap_var, 0, 0, chk_bg)
        self._make_chk(chk_frame, "Строчные",     self.low_var, 0, 1, chk_bg)
        self._make_chk(chk_frame, "Цифры",        self.dig_var, 1, 0, chk_bg)
        self._make_chk(chk_frame, "Спецсимволы",  self.sym_var, 1, 1, chk_bg)

        # ── Кнопка генерации ────────────────────────────────────
        self.gen_btn = self._make_btn(self, "🚀  Сгенерировать",
                                       "#a855f7", self._generate)
        self.gen_btn.pack(fill="x", padx=28, pady=(4, 10), ipady=6)

        # ── Поле пароля ─────────────────────────────────────────
        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(self, textvariable=self.pwd_var,
                                   font=font_pwd,
                                   relief="sunken", bd=2,
                                   bg="#ffffff", fg="#1a1a1a",
                                   state="readonly")
        self.pwd_entry.pack(fill="x", padx=28, pady=(0, 6), ipady=6)

        # ── Индикатор надёжности ────────────────────────────────
        self.strength_var = tk.StringVar()
        tk.Label(self, textvariable=self.strength_var,
                 font=("Helvetica", 9), bg=bg,
                 fg="#888888").pack(anchor="w", padx=28, pady=(0, 6))

        # ── Кнопка копирования ──────────────────────────────────
        self.copy_btn = self._make_btn(self, "📋  Скопировать",
                                        "#a78bfa", self._copy_password)
        self.copy_btn.pack(fill="x", padx=28, pady=(0, 24), ipady=6)

    # ── Вспомогательные методы ──────────────────────────────────

    def _row_label(self, text, padx):
        tk.Label(self, text=text,
                 font=("Helvetica", 11), bg="#f8f8ff",
                 fg="#1a1a1a").pack(anchor="w", padx=padx)

    def _make_chk(self, parent, text, var, row, col, bg):
        cb = tk.Checkbutton(parent, text=text, variable=var,
                             font=("Helvetica", 10),
                             bg=bg, fg="#1a1a1a",
                             selectcolor="#ffffff",
                             activebackground=bg,
                             relief="flat")
        cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=2)

    def _make_btn(self, parent, text, color, command):
        """Кнопка с тиснением (raised) и сиреневым градиентным эффектом."""
        btn = tk.Button(parent, text=text, command=command,
                         font=("Helvetica", 11, "bold"),
                         bg=color, fg="#ffffff",
                         activebackground="#c084fc",
                         activeforeground="#ffffff",
                         relief="raised", bd=3,
                         highlightbackground="#7c3aed",
                         cursor="hand2",
                         padx=10, pady=6)
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

            # Обновить список
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

        old_text = self.copy_btn["text"]
        self.copy_btn.config(text="✓ Скопировано!")
        self.after(1500, lambda: self.copy_btn.config(text=old_text))

    def _on_close(self):
        self._save_data()
        self.destroy()


if __name__ == "__main__":
    app = PassGenApp()
    app.mainloop()
