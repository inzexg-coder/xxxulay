import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_password
from settings import load_services, save_services, load_settings, save_settings

# -- Font detection -------------------------------------------------
FONT_CANDIDATES = [
    ("Liberation Sans", 13),
    ("DejaVu Sans", 13),
    ("Noto Sans", 13),
]

MONO_CANDIDATES = [
    "Liberation Mono",
    "DejaVu Sans Mono",
    "Noto Sans Mono",
    "Courier New",
    "Courier",
]


def _font_exists(family, size):
    try:
        f = font.Font(family=family, size=size)
        return f.actual("family") == family
    except Exception:
        return False


def _pick_fonts():
    base = ("TkDefaultFont", 13)
    for family, size in FONT_CANDIDATES:
        if _font_exists(family, size):
            base = (family, size)
            break

    mono = ("TkFixedFont", 13)
    for family in MONO_CANDIDATES:
        if _font_exists(family, 13):
            mono = (family, 13)
            break

    return base, mono


# -- Colors ---------------------------------------------------------
BG         = "#f8f8ff"
FG         = "#1a1a1a"
BTN_LILAC  = "#a855f7"
BTN_HVR    = "#c084fc"
BTN_EDGE   = "#7c3aed"
BTN_VIOLET = "#a78bfa"
ENTRY_BG   = "#ffffff"
MUTED      = "#888888"


class PassGenApp(tk.Tk):
    """Main window."""

    def __init__(self):
        super().__init__()
        self.title("passgen")
        self.configure(bg=BG)

        win_w, win_h = 400, 480
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{win_w}x{win_h}+{(sw-win_w)//2}+{(sh-win_h)//2}")
        self.resizable(False, False)

        self._base_font, self._mono_font = _pick_fonts()

        self._build_ui()
        self._load_data()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # -- UI ---------------------------------------------------------

    def _build_ui(self):
        self.configure(bg=BG)

        FONT_REG    = (self._base_font[0], self._base_font[1], "normal")
        FONT_BOLD   = (self._base_font[0], self._base_font[1], "bold")
        FONT_TITLE  = (self._base_font[0], 18, "bold")
        FONT_PWD    = (self._mono_font[0], self._mono_font[1], "bold")

        # Title
        tk.Label(self, text="passgen  -  Password Generator",
                 font=FONT_TITLE, bg=BG, fg="#4a1a6b"
        ).pack(anchor="w", padx=28, pady=(22, 18))

        # Master seed
        self._label("Master seed:", FONT_BOLD)
        self.seed_var = tk.StringVar()
        self.seed_entry = self._entry(self.seed_var, FONT_REG)
        self.seed_entry.pack(fill="x", padx=28, pady=(0, 10), ipady=6)
        self.seed_entry.bind("<KeyRelease>", lambda e: self._clear_error())

        # Error label
        self.error_var = tk.StringVar()
        self.error_label = tk.Label(self, textvariable=self.error_var, font=FONT_REG, bg=BG, fg="#e03131")
        self.error_label.pack(anchor="w", padx=28, pady=(0, 4))

        # Service
        self._label("Service:", FONT_BOLD)
        self.svc_var = tk.StringVar()
        self.svc_combo = ttk.Combobox(self, textvariable=self.svc_var,
                                       font=FONT_REG)
        self.svc_combo.pack(fill="x", padx=28, pady=(0, 10))
        self.svc_combo.bind("<Return>", lambda e: self._generate())
        self.svc_combo.bind("<KP_Enter>", lambda e: self._generate())
        self.svc_combo.bind("<<ComboboxSelected>>", lambda e: self._clear_error())
        self.svc_combo.bind("<KeyRelease>", lambda e: self._clear_error())

        # Length
        frame_len = tk.Frame(self, bg=BG)
        frame_len.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_len, text="Length:", font=FONT_BOLD,
                 bg=BG, fg=FG).pack(side="left")
        self.len_var = tk.IntVar(value=10)
        self.len_spin = tk.Spinbox(frame_len, from_=1, to=99,
                                    textvariable=self.len_var,
                                    font=FONT_BOLD, width=6,
                                    relief="sunken", bd=2,
                                    bg=ENTRY_BG, fg=FG)
        self.len_spin.pack(side="right")

        # Checkboxes
        frame_chk = tk.Frame(self, bg=BG)
        frame_chk.pack(fill="x", padx=28, pady=(0, 12))
        tk.Label(frame_chk, text="Charset:", font=FONT_BOLD,
                 bg=BG, fg=FG).grid(row=0, column=0, sticky="nw",
                                    padx=(0, 18), pady=(2, 0))

        self.cap_var = tk.BooleanVar(value=True)
        self.low_var = tk.BooleanVar(value=True)
        self.dig_var = tk.BooleanVar(value=False)
        self.sym_var = tk.BooleanVar(value=True)

        chk_frame = tk.Frame(frame_chk, bg=BG)
        chk_frame.grid(row=0, column=1, sticky="w")

        self._chk(chk_frame, "Capitals",  self.cap_var, 0, 0, FONT_REG)
        self._chk(chk_frame, "Lowercase", self.low_var, 0, 1, FONT_REG)
        self._chk(chk_frame, "Digits",    self.dig_var, 1, 0, FONT_REG)
        self._chk(chk_frame, "Symbols",   self.sym_var, 1, 1, FONT_REG)

        # Generate button
        self.gen_btn = self._btn("Generate", FONT_BOLD,
                                 BTN_LILAC, self._generate)
        self.gen_btn.pack(fill="x", padx=28, pady=(4, 10), ipady=8)

        # Password field
        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(self, textvariable=self.pwd_var,
                                   font=FONT_PWD,
                                   relief="sunken", bd=2,
                                   bg=ENTRY_BG, fg=FG,
                                   state="readonly")
        self.pwd_entry.pack(fill="x", padx=28, pady=(0, 6), ipady=8)

        # Strength indicator
        self.strength_var = tk.StringVar()
        tk.Label(self, textvariable=self.strength_var,
                 font=FONT_BOLD, bg=BG, fg=MUTED
        ).pack(anchor="w", padx=28, pady=(0, 6))

        # Copy button
        self.copy_btn = self._btn("Copy", FONT_BOLD,
                                  BTN_VIOLET, self._copy_password)
        self.copy_btn.pack(fill="x", padx=28, pady=(0, 24), ipady=8)

    # -- Widget helpers ---------------------------------------------

    def _label(self, text, font):
        tk.Label(self, text=text, font=font, bg=BG, fg=FG
        ).pack(anchor="w", padx=28)

    def _entry(self, var, font):
        return tk.Entry(self, textvariable=var, font=font,
                         relief="sunken", bd=2,
                         bg=ENTRY_BG, fg=FG)

    def _chk(self, parent, text, var, row, col, font):
        cb = tk.Checkbutton(parent, text=text, variable=var,
                             font=font, bg=BG, fg=FG,
                             selectcolor=ENTRY_BG,
                             activebackground=BG, relief="flat")
        cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=2)

    def _btn(self, text, font, color, command):
        btn = tk.Button(self, text=text, command=command,
                         font=font,
                         bg=color, fg="#ffffff",
                         activebackground=BTN_HVR,
                         activeforeground="#ffffff",
                         relief="raised", bd=3,
                         highlightbackground=BTN_EDGE,
                         cursor="hand2")
        return btn

    # -- Load / Save -------------------------------------------------

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

    # -- Logic -------------------------------------------------------

    def _generate(self):
        service = self.svc_var.get().strip()
        seed = self.seed_var.get().strip()

        if not seed:
            self.error_var.set("Enter master seed")
            return
        if not service:
            self.error_var.set("Enter service name")
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
            self._clear_error()

            vals = list(self.svc_combo["values"])
            if service not in vals:
                vals.append(service)
                self.svc_combo["values"] = vals

        except ValueError as ex:
            messagebox.showwarning("", str(ex))

    def _clear_error(self):
        if self.error_var.get():
            self.error_var.set("")

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
