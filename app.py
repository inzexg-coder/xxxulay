import tkinter as tk
from tkinter import ttk, font
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_password
from settings import load_services, save_services, load_settings, save_settings

# ── Font detection ──────────────────────────────────────────────
FONT_CANDIDATES = [
    ("Roboto", 12),            # Material Design (ttf-roboto)
    ("Liberation Sans", 12),
    ("DejaVu Sans", 12),
    ("Noto Sans", 12),
]
MONO_CANDIDATES = [
    "Roboto Mono",
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
    except: return False

def _pick_fonts():
    base = ("TkDefaultFont", 12)
    for f, s in FONT_CANDIDATES:
        if _font_exists(f, s): base = (f, s); break
    mono = ("TkFixedFont", 12)
    for f in MONO_CANDIDATES:
        if _font_exists(f, 12): mono = (f, 12); break
    return base, mono

# ── Material circular checkbox ──────────────────────────────────
class MaterialCheckbox(tk.Frame):
    """Circular toggle (radio‑like circle) with text."""

    def __init__(self, parent, text="", variable=None, command=None, **kw):
        if "bg" not in kw: kw["bg"] = parent["bg"]
        super().__init__(parent, **kw)
        self._var = variable if variable is not None else tk.BooleanVar()
        self._command = command
        self._size = 20

        self._canvas = tk.Canvas(self, width=self._size, height=self._size,
                                  bg=self["bg"], highlightthickness=0)
        self._canvas.pack(side="left")
        self._draw_circle()

        self._label = tk.Label(self, text=text, bg=self["bg"],
                                fg="#1a1a1a", font=("TkDefaultFont", 11))
        self._label.pack(side="left", padx=(6, 0))

        self._canvas.bind("<Button-1>", self._toggle)
        self._label.bind("<Button-1>", self._toggle)

    def _draw_circle(self):
        self._canvas.delete("all")
        r = self._size // 2
        cx = cy = r
        if self._var.get():
            # filled circle
            self._canvas.create_oval(2, 2, self._size-2, self._size-2,
                                      outline="#a855f7", width=2, fill="#a855f7")
            self._canvas.create_oval(6, 6, self._size-6, self._size-6,
                                      outline="#ffffff", fill="#ffffff")
        else:
            self._canvas.create_oval(2, 2, self._size-2, self._size-2,
                                      outline="#888888", width=2)

    def _toggle(self, event=None):
        self._var.set(not self._var.get())
        self._draw_circle()
        if self._command: self._command()

    def get(self): return self._var.get()
    def set(self, v): self._var.set(v); self._draw_circle()

# ── Tooltip ─────────────────────────────────────────────────────
class ToolTip:
    def __init__(self, widget, text, delay=400):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._tip = None
        self._after_id = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)

    def _schedule(self, e=None):
        self._after_id = self.widget.after(self.delay, self._show)

    def _show(self):
        if self._tip: return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        tk.Label(self._tip, text=self.text, justify="left",
                 bg="#eaddff", fg="#1a1a1a",
                 font=("TkDefaultFont", 10),
                 relief="solid", bd=1, padx=8, pady=4).pack()

    def _hide(self, e=None):
        if self._after_id: self.widget.after_cancel(self._after_id); self._after_id = None
        if self._tip: self._tip.destroy(); self._tip = None

# ── Colors ──────────────────────────────────────────────────────
BG       = "#f8f8ff"
CARD_BG  = "#ffffff"
FG       = "#1a1a1a"
PURPLE   = "#a855f7"
PURPLE2  = "#7c3aed"
VIOLET   = "#a78bfa"
HVR      = "#c084fc"
ERR      = "#e03131"
MUTED    = "#888888"
SUBTLE   = "#dddddd"

# ── App ─────────────────────────────────────────────────────────
class PassGenApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("passgen")
        self.configure(bg=BG)
        self._bf, self._mf = _pick_fonts()

        win_w, win_h = 420, 520
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{win_w}x{win_h}+{(sw-win_w)//2}+{(sh-win_h)//2}")
        self.resizable(False, False)

        self._build_ui()
        self._load_data()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI ──────────────────────────────────────────────────────

    def _card(self, parent, title):
        """A card frame with rounded‑ish look."""
        card = tk.Frame(parent, bg=CARD_BG, bd=1, relief="solid", highlightbackground=SUBTLE)
        if title:
            tk.Label(card, text=title, font=(self._bf[0], 10, "bold"),
                     bg=CARD_BG, fg=MUTED).pack(anchor="w", padx=16, pady=(12, 0))
            ttk.Separator(card, orient="horizontal").pack(fill="x", padx=12, pady=(6, 8))
        return card

    def _build_ui(self):
        self.configure(bg=BG)
        F_REG    = (self._bf[0], self._bf[1])
        F_BOLD   = (self._bf[0], self._bf[1], "bold")
        F_TITLE  = (self._bf[0], 18, "bold")
        F_PWD    = (self._mf[0], self._mf[1], "bold")

        # ── Header ──
        tk.Label(self, text="passgen", font=F_TITLE,
                 bg=BG, fg="#4a1a6b").pack(anchor="w", padx=24, pady=(20, 12))

        # ── Card: Credentials ──
        card1 = self._card(self, "CREDENTIALS")
        card1.pack(fill="x", padx=20, pady=(0, 10))

        f1 = tk.Frame(card1, bg=CARD_BG)
        f1.pack(fill="x", padx=16, pady=(0, 12))

        tk.Label(f1, text="Master seed", font=F_BOLD, bg=CARD_BG, fg=FG
        ).grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.seed_var = tk.StringVar()
        self.seed_entry = tk.Entry(f1, textvariable=self.seed_var, font=F_REG,
                                    relief="solid", bd=1, highlightbackground=SUBTLE,
                                    bg="#ffffff", fg=FG)
        self.seed_entry.grid(row=1, column=0, sticky="ew", ipady=5)
        self.seed_entry.bind("<KeyRelease>", lambda e: self._clear_error())
        ToolTip(self.seed_entry, "Your secret phrase. Keep it in your head.")

        self.error_var = tk.StringVar()
        tk.Label(f1, textvariable=self.error_var, font=F_REG,
                 bg=CARD_BG, fg=ERR).grid(row=2, column=0, sticky="w")
        f1.columnconfigure(0, weight=1)

        # ── Card: Service ──
        card2 = self._card(self, "SERVICE")
        card2.pack(fill="x", padx=20, pady=(0, 10))

        f2 = tk.Frame(card2, bg=CARD_BG)
        f2.pack(fill="x", padx=16, pady=(0, 12))

        tk.Label(f2, text="Service name", font=F_BOLD, bg=CARD_BG, fg=FG
        ).grid(row=0, column=0, sticky="w", pady=(0, 2))

        svc_frame = tk.Frame(f2, bg=CARD_BG)
        svc_frame.grid(row=1, column=0, sticky="ew")
        self.svc_var = tk.StringVar()
        self.svc_entry = tk.Entry(svc_frame, textvariable=self.svc_var, font=F_REG,
                                   relief="solid", bd=1, highlightbackground=SUBTLE,
                                   bg="#ffffff", fg=FG)
        self.svc_entry.pack(side="left", fill="x", expand=True, ipady=5)
        self.svc_entry.bind("<Return>", lambda e: self._generate())
        self.svc_entry.bind("<KeyRelease>", lambda e: self._clear_error())
        ToolTip(self.svc_entry,
                "Website or app name.\nExamples: google, vk, github")

        # Arrow button for saved services
        self.svc_arrow = tk.Label(svc_frame, text="\u25BE",
                                  font=("TkDefaultFont", 14),
                                  bg=CARD_BG, fg=PURPLE, cursor="hand2")
        self.svc_arrow.pack(side="right", padx=(4, 0))
        self.svc_arrow.bind("<Enter>", self._show_service_menu)
        self.svc_arrow.bind("<Leave>", lambda e:
            self.after(300, self._hide_service_menu))
        self._svc_menu = None

        f2.columnconfigure(0, weight=1)

        # Row: Length + Charset labels
        card3 = self._card(self, "OPTIONS")
        card3.pack(fill="x", padx=20, pady=(0, 10))

        f3 = tk.Frame(card3, bg=CARD_BG)
        f3.pack(fill="x", padx=16, pady=(0, 12))

        # Length
        tk.Label(f3, text="Length", font=F_BOLD, bg=CARD_BG, fg=FG
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.len_var = tk.IntVar(value=10)
        len_frame = tk.Frame(f3, bg=CARD_BG)
        len_frame.grid(row=1, column=0, sticky="w")
        self.len_entry = tk.Entry(len_frame, textvariable=self.len_var,
                                   font=F_BOLD, width=5,
                                   relief="solid", bd=1, highlightbackground=SUBTLE,
                                   bg="#ffffff", fg=FG, justify="center")
        self.len_entry.pack(side="left", ipady=4)

        # Manual up/down buttons
        btn_frame = tk.Frame(len_frame, bg=CARD_BG)
        btn_frame.pack(side="left", padx=(2, 0))
        self._arrow_btn(btn_frame, "\u25B2", lambda: self._adj_len(1)).pack()
        self._arrow_btn(btn_frame, "\u25BC", lambda: self._adj_len(-1)).pack()
        ToolTip(len_frame, "Password length (recommended: 12-16)")

        # Charset checkboxes (circular)
        tk.Label(f3, text="Characters", font=F_BOLD, bg=CARD_BG, fg=FG
        ).grid(row=0, column=1, sticky="w", padx=(30, 0), pady=(0, 4))

        chk_frame = tk.Frame(f3, bg=CARD_BG)
        chk_frame.grid(row=1, column=1, sticky="w", padx=(30, 0))

        self.cap_v = tk.BooleanVar(value=True)
        self.low_v = tk.BooleanVar(value=True)
        self.dig_v = tk.BooleanVar(value=False)
        self.sym_v = tk.BooleanVar(value=True)

        self._mchk(chk_frame, "Capitals",  self.cap_v, "A B C D ...").grid(row=0, column=0, padx=(0, 12))
        self._mchk(chk_frame, "Lowercase", self.low_v, "a b c d ...").grid(row=0, column=1, padx=(0, 12))
        self._mchk(chk_frame, "Digits",    self.dig_v, "0 1 2 3 ...").grid(row=1, column=0, padx=(0, 12), pady=(6, 0))
        self._mchk(chk_frame, "Symbols",   self.sym_v, "! @ # $ ...").grid(row=1, column=1, padx=(0, 0), pady=(6, 0))

        f3.columnconfigure(0, weight=0)
        f3.columnconfigure(1, weight=1)

        # ── Generate button ──
        self.gen_btn = tk.Button(self, text="Generate", font=F_BOLD,
                                  bg=PURPLE, fg="#ffffff",
                                  activebackground=HVR, activeforeground="#ffffff",
                                  relief="flat", bd=0, cursor="hand2",
                                  command=self._generate)
        self.gen_btn.pack(fill="x", padx=20, pady=(0, 10), ipady=8)
        ToolTip(self.gen_btn, "Create a unique password.")

        # ── Password card ──
        card4 = self._card(self, "PASSWORD")
        card4.pack(fill="x", padx=20, pady=(0, 10))

        f4 = tk.Frame(card4, bg=CARD_BG)
        f4.pack(fill="x", padx=16, pady=(0, 12))

        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(f4, textvariable=self.pwd_var, font=F_PWD,
                                   relief="solid", bd=1, highlightbackground=SUBTLE,
                                   bg="#ffffff", fg=FG, state="readonly")
        self.pwd_entry.pack(fill="x", ipady=6)
        ToolTip(self.pwd_entry, "Your generated password.\nPress Copy.")

        # Strength
        self.strength_var = tk.StringVar()
        tk.Label(f4, textvariable=self.strength_var,
                 font=F_REG, bg=CARD_BG, fg=MUTED
        ).pack(anchor="w", pady=(4, 0))

        # ── Copy button ──
        self.copy_btn = tk.Button(self, text="Copy", font=F_BOLD,
                                   bg=VIOLET, fg="#ffffff",
                                   activebackground=HVR, activeforeground="#ffffff",
                                   relief="flat", bd=0, cursor="hand2",
                                   command=self._copy_password)
        self.copy_btn.pack(fill="x", padx=20, pady=(0, 24), ipady=8)
        ToolTip(self.copy_btn, "Copy to clipboard.")

    # ── Helpers ─────────────────────────────────────────────────

    def _mchk(self, parent, text, var, tip):
        f = tk.Frame(parent, bg=CARD_BG)
        cb = MaterialCheckbox(f, text=text, variable=var, bg=CARD_BG)
        cb.pack()
        ToolTip(cb, tip)
        return f

    def _arrow_btn(self, parent, char, cmd):
        lbl = tk.Label(parent, text=char, font=("TkDefaultFont", 8),
                        bg=CARD_BG, fg=PURPLE, cursor="hand2")
        lbl.bind("<Button-1>", lambda e: cmd())
        return lbl

    def _adj_len(self, delta):
        v = self.len_var.get() + delta
        if 1 <= v <= 99:
            self.len_var.set(v)

    # ── Service dropdown ────────────────────────────────────────

    def _show_service_menu(self, event=None):
        svcs = list(self.svc_combo_values) if hasattr(self, 'svc_combo_values') else []
        if not svcs:
            return
        if self._svc_menu:
            self._svc_menu.destroy()
        x = self.svc_arrow.winfo_rootx()
        y = self.svc_arrow.winfo_rooty() + self.svc_arrow.winfo_height()
        self._svc_menu = tk.Toplevel(self)
        self._svc_menu.wm_overrideredirect(True)
        self._svc_menu.wm_geometry(f"+{x}+{y}")
        lb = tk.Listbox(self._svc_menu, font=(self._bf[0], 10),
                        bg="#ffffff", fg=FG,
                        relief="solid", bd=1, highlightthickness=0,
                        activestyle="none",
                        width=20, height=min(len(svcs), 8))
        lb.pack()
        for s in svcs:
            lb.insert("end", s)
        lb.bind("<Button-1>", lambda e: self._pick_service(lb, lb.nearest(e.y)))
        self._svc_lb = lb

    def _pick_service(self, lb, idx):
        if idx >= 0:
            self.svc_var.set(lb.get(idx))
            self._clear_error()
        self._hide_service_menu()

    def _hide_service_menu(self):
        if self._svc_menu:
            self._svc_menu.destroy()
            self._svc_menu = None

    # ── Data ────────────────────────────────────────────────────

    def _load_data(self):
        s = load_settings()
        self.len_var.set(s["length"])
        self.cap_v.set(s["capitals"])
        self.low_v.set(s["lower"])
        self.dig_v.set(s["digits"])
        self.sym_v.set(s["symbols"])
        svcs = load_services()
        if svcs:
            self.svc_combo_values = svcs
            self.svc_arrow.configure(fg=PURPLE)
        else:
            self.svc_combo_values = []
            self.svc_arrow.configure(fg=CARD_BG)

    def _save_data(self):
        save_settings(
            length=self.len_var.get(),
            capitals=self.cap_v.get(),
            lower=self.low_v.get(),
            digits=self.dig_v.get(),
            symbols=self.sym_v.get(),
        )
        svcs = getattr(self, 'svc_combo_values', [])
        cur = self.svc_var.get().strip()
        if cur and cur not in svcs:
            svcs.append(cur)
        save_services(svcs)

    # ── Logic ───────────────────────────────────────────────────

    def _generate(self):
        service = self.svc_var.get().strip()
        seed = self.seed_var.get().strip()
        if not seed:
            self.error_var.set("Enter master seed"); return
        if not service:
            self.error_var.set("Enter service name"); return
        try:
            pwd = generate_password(
                master_seed=seed, service=service,
                length=self.len_var.get(),
                use_capitals=self.cap_v.get(),
                use_lower=self.low_v.get(),
                use_digits=self.dig_v.get(),
                use_symbols=self.sym_v.get(),
            )
            self.pwd_var.set(pwd)
            self._clear_error()
            svcs = getattr(self, 'svc_combo_values', [])
            if service not in svcs:
                svcs.append(service)
                self.svc_combo_values = svcs
                self.svc_arrow.configure(fg=PURPLE)
        except ValueError:
            self.error_var.set("Select at least one character type")

    def _clear_error(self):
        if self.error_var.get(): self.error_var.set("")

    def _copy_password(self):
        pwd = self.pwd_var.get()
        if not pwd: return
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
