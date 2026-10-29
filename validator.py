# Модуль валидации — проверяем данные сотрудников перед обработкой
# Защищаем систему от некорректных данных в CSV файле

from datetime import datetime

MAKS_ZARPLATA = 1000000     # максимальная зарплата для проверки
MIN_ZARPLATA = 10000        # минимальная зарплата для проверки
MAKS_DLINA_IMENI = 100      # максимальная длина имени


def proverit_imya(imya):
    imya = imya.strip()
    if not imya:
        raise ValueError("Имя сотрудника не может быть пустым")
    if len(imya) > MAKS_DLINA_IMENI:
        raise ValueError(f"Имя слишком длинное: {len(imya)} символов")
    if any(c.isdigit() for c in imya):
        raise ValueError(f"Имя содержит цифры: '{imya}'")
    return imya


def proverit_zarplatu(zarplata):
    try:
        z = float(str(zarplata).replace(",", "."))
    except ValueError:
        raise ValueError(f"Зарплата должна быть числом: '{zarplata}'")
    if z < MIN_ZARPLATA:
        raise ValueError(f"Зарплата {z} ниже минимальной ({MIN_ZARPLATA})")
    if z > MAKS_ZARPLATA:
        raise ValueError(f"Зарплата {z} выше максимальной ({MAKS_ZARPLATA})")
    return z


def proverit_datu(data):
    data = data.strip()
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Неверный формат даты '{data}', ожидается ГГГГ-ММ-ДД")
    return data


def proverit_otdel(otdel):
    otdel = otdel.strip()
    if not otdel:
        raise ValueError("Название отдела не может быть пустым")
    return otdel