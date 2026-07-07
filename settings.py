"""
settings.py — Загрузка и сохранение настроек и истории сервисов.

Форматы файлов совместимы с оригинальной C#-версией:
  settings.txt  → CSV: длина,заглавные,строчные,цифры,спецсимволы
  services.txt  → по одному сервису на строку
"""

import os

SERVICES_FILE = "services.txt"
SETTINGS_FILE = "settings.txt"

# ----------------------------------------------------------------
# Сервисы (история)
# ----------------------------------------------------------------

def load_services() -> list[str]:
    """Загрузить список сервисов из services.txt."""
    services: list[str] = []
    if not os.path.exists(SERVICES_FILE):
        return services
    try:
        with open(SERVICES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    services.append(line)
    except (OSError, IOError):
        pass
    return services


def save_services(services: list[str]) -> None:
    """Сохранить список сервисов в services.txt."""
    try:
        with open(SERVICES_FILE, "w", encoding="utf-8") as f:
            for s in services:
                f.write(s + "\n")
    except (OSError, IOError):
        pass


# ----------------------------------------------------------------
# Настройки (длина + флаги символов)
# ----------------------------------------------------------------

DEFAULT_SETTINGS = {
    "length": 8,
    "capitals": True,
    "lower": True,
    "digits": False,
    "symbols": True,
}


def load_settings() -> dict:
    """Загрузить настройки из settings.txt (с защитой от ошибок)."""
    settings = dict(DEFAULT_SETTINGS)
    if not os.path.exists(SETTINGS_FILE):
        return settings

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            line = f.readline().strip()
        if not line:
            return settings

        parts = line.split(",")
        if len(parts) >= 5:
            settings["length"] = max(1, int(parts[0]))
            settings["capitals"] = parts[1] == "1"
            settings["lower"] = parts[2] == "1"
            settings["digits"] = parts[3] == "1"
            settings["symbols"] = parts[4] == "1"
    except (ValueError, IndexError, OSError):
        # При повреждённом файле — тихо возвращаем умолчания
        pass

    return settings


def save_settings(length: int, capitals: bool, lower: bool,
                  digits: bool, symbols: bool) -> None:
    """Сохранить настройки в settings.txt (CSV, совместимо с C#)."""
    config = (
        f"{length},"
        f"{'1' if capitals else '0'},"
        f"{'1' if lower else '0'},"
        f"{'1' if digits else '0'},"
        f"{'1' if symbols else '0'}"
    )
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            f.write(config + "\n")
    except (OSError, IOError):
        pass
