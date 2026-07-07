"""
app.py — WinForms GUI для детерминированного генератора паролей.

Использует pythonnet (модуль clr) для вызова .NET Windows Forms.
Запуск: python app.py
"""

import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (
    Application, Form, FormBorderStyle,
    Label, TextBox, ComboBox, CheckBox, NumericUpDown, Button,
    Clipboard, MessageBox, MessageBoxButtons, MessageBoxIcon,
    ContentAlignment, Keys,
)
from System.Drawing import Point, Size
from System import Decimal as DotNetDecimal

# Путь к модулям — они лежат рядом с app.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import generate_password
from settings import load_services, save_services, load_settings, save_settings


class PassGenForm(Form):
    """Главное окно генератора паролей."""

    def __init__(self):
        self.Text = "passgen"
        self.ClientSize = Size(294, 299)
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.MaximizeBox = False

        self._create_controls()
        self._load_data()

    # ── Создание контролов ──────────────────────────────────────

    def _create_controls(self):
        # Метка: Сид-фраза
        self.lbl_seed = Label()
        self.lbl_seed.Text = "Сид-фраза:"
        self.lbl_seed.Location = Point(0, 10)
        self.lbl_seed.Size = Size(120, 16)
        self.lbl_seed.TextAlign = ContentAlignment.MiddleRight

        # Поле ввода сид-фразы
        self.tb_seed = TextBox()
        self.tb_seed.Location = Point(136, 8)
        self.tb_seed.Size = Size(152, 20)

        # Метка: Название сервиса
        self.lbl_service = Label()
        self.lbl_service.Text = "Название сервиса:"
        self.lbl_service.Location = Point(0, 42)
        self.lbl_service.Size = Size(120, 16)
        self.lbl_service.TextAlign = ContentAlignment.MiddleRight

        # ComboBox для выбора/ввода сервиса
        self.cmb_service = ComboBox()
        self.cmb_service.Location = Point(136, 40)
        self.cmb_service.Size = Size(152, 21)
        self.cmb_service.KeyDown += self._cmb_service_keydown

        # Метка: Длина
        self.lbl_length = Label()
        self.lbl_length.Text = "Длина:"
        self.lbl_length.Location = Point(0, 74)
        self.lbl_length.Size = Size(120, 16)
        self.lbl_length.TextAlign = ContentAlignment.MiddleRight

        # Числовой ввод длины пароля
        self.num_length = NumericUpDown()
        self.num_length.Location = Point(136, 72)
        self.num_length.Size = Size(40, 20)
        self.num_length.Minimum = DotNetDecimal(1)
        self.num_length.Maximum = DotNetDecimal(99)
        self.num_length.Value = DotNetDecimal(10)

        # Метка: Символы
        self.lbl_symbols = Label()
        self.lbl_symbols.Text = "Символы:"
        self.lbl_symbols.Location = Point(0, 104)
        self.lbl_symbols.Size = Size(120, 16)
        self.lbl_symbols.TextAlign = ContentAlignment.MiddleRight

        # Чекбокс: Заглавные буквы
        self.cb_capital = CheckBox()
        self.cb_capital.Text = "Заглавные буквы"
        self.cb_capital.Location = Point(136, 104)
        self.cb_capital.Size = Size(128, 24)
        self.cb_capital.Checked = True

        # Чекбокс: Строчные буквы
        self.cb_lower = CheckBox()
        self.cb_lower.Text = "Строчные буквы"
        self.cb_lower.Location = Point(136, 128)
        self.cb_lower.Size = Size(128, 24)
        self.cb_lower.Checked = True

        # Чекбокс: Цифры
        self.cb_digits = CheckBox()
        self.cb_digits.Text = "Цифры"
        self.cb_digits.Location = Point(136, 152)
        self.cb_digits.Size = Size(128, 24)

        # Чекбокс: Спецсимволы
        self.cb_symbols = CheckBox()
        self.cb_symbols.Text = "Спецсимволы"
        self.cb_symbols.Location = Point(136, 176)
        self.cb_symbols.Size = Size(128, 24)
        self.cb_symbols.Checked = True

        # Кнопка: Готово (генерация)
        self.btn_generate = Button()
        self.btn_generate.Text = "Готово"
        self.btn_generate.Location = Point(8, 208)
        self.btn_generate.Size = Size(280, 23)
        self.btn_generate.Click += self._btn_generate_click

        # Поле вывода пароля (только для чтения)
        self.tb_password = TextBox()
        self.tb_password.Location = Point(8, 240)
        self.tb_password.Size = Size(280, 20)
        self.tb_password.ReadOnly = True
        self.tb_password.KeyDown += self._tb_password_keydown

        # Кнопка: Скопировать
        self.btn_copy = Button()
        self.btn_copy.Text = "Скопировать"
        self.btn_copy.Location = Point(8, 272)
        self.btn_copy.Size = Size(280, 23)
        self.btn_copy.Click += self._btn_copy_click

        # Собираем всё на форму
        self.Controls.Add(self.lbl_seed)
        self.Controls.Add(self.tb_seed)
        self.Controls.Add(self.lbl_service)
        self.Controls.Add(self.cmb_service)
        self.Controls.Add(self.lbl_length)
        self.Controls.Add(self.num_length)
        self.Controls.Add(self.lbl_symbols)
        self.Controls.Add(self.cb_capital)
        self.Controls.Add(self.cb_lower)
        self.Controls.Add(self.cb_digits)
        self.Controls.Add(self.cb_symbols)
        self.Controls.Add(self.btn_generate)
        self.Controls.Add(self.tb_password)
        self.Controls.Add(self.btn_copy)

    # ── Загрузка / сохранение данных ────────────────────────────

    def _load_data(self):
        settings = load_settings()
        self.num_length.Value = DotNetDecimal(settings["length"])
        self.cb_capital.Checked = settings["capitals"]
        self.cb_lower.Checked = settings["lower"]
        self.cb_digits.Checked = settings["digits"]
        self.cb_symbols.Checked = settings["symbols"]

        for svc in load_services():
            self.cmb_service.Items.Add(svc)

    def _save_data(self):
        save_settings(
            length=int(self.num_length.Value),
            capitals=self.cb_capital.Checked,
            lower=self.cb_lower.Checked,
            digits=self.cb_digits.Checked,
            symbols=self.cb_symbols.Checked,
        )
        services = [
            str(self.cmb_service.Items[i])
            for i in range(self.cmb_service.Items.Count)
        ]
        save_services(services)

    # ── Обработчики событий ─────────────────────────────────────

    def _cmb_service_keydown(self, sender, e):
        if e.KeyCode == Keys.Enter:
            self._generate()

    def _tb_password_keydown(self, sender, e):
        if e.KeyCode == Keys.Enter:
            self._copy_password()
            self.ActiveControl = self.cmb_service

    def _btn_generate_click(self, sender, e):
        self._generate()

    def _btn_copy_click(self, sender, e):
        self._copy_password()

    def _generate(self):
        service = self.cmb_service.Text

        # Добавить сервис в историю, если новый
        if service:
            found = False
            for i in range(self.cmb_service.Items.Count):
                if str(self.cmb_service.Items[i]) == service:
                    found = True
                    break
            if not found:
                self.cmb_service.Items.Add(service)

        master_seed = self.tb_seed.Text
        if not master_seed:
            MessageBox.Show(
                "Введите сид-фразу",
                "Ошибка",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning,
            )
            return

        length = int(self.num_length.Value)

        try:
            password = generate_password(
                master_seed=master_seed,
                service=service,
                length=length,
                use_capitals=self.cb_capital.Checked,
                use_lower=self.cb_lower.Checked,
                use_digits=self.cb_digits.Checked,
                use_symbols=self.cb_symbols.Checked,
            )
            self.tb_password.Text = password
            self.ActiveControl = self.tb_password
        except ValueError as ex:
            MessageBox.Show(
                str(ex), "Ошибка",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning,
            )

    def _copy_password(self):
        if self.tb_password.Text:
            Clipboard.SetText(self.tb_password.Text)

    # ── Закрытие формы ──────────────────────────────────────────

    def OnFormClosing(self, e):
        self._save_data()
        super().OnFormClosing(e)


if __name__ == "__main__":
    Application.EnableVisualStyles()
    Application.SetCompatibleTextRenderingDefault(False)
    Application.Run(PassGenForm())
