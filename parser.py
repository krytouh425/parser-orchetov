# Модель сотрудника — основная единица данных в системе
# Используется всеми модулями парсера отчётов

from datetime import datetime


class Sotrudnik:
    def __init__(self, imya, otdel, dolzhnost, zarplata, data_priema):
        self.imya = imya
        self.otdel = otdel
        self.dolzhnost = dolzhnost
        self.zarplata = float(zarplata)
        self.data_priema = data_priema  # формат: ГГГГ-ММ-ДД

    def stazh_let(self):
        # считаем стаж от даты приёма до сегодня
        data = datetime.strptime(self.data_priema, "%Y-%m-%d")
        delta = datetime.now() - data
        return round(delta.days / 365, 1)

    def to_dict(self):
        return {
            "imya": self.imya,
            "otdel": self.otdel,
            "dolzhnost": self.dolzhnost,
            "zarplata": self.zarplata,
            "data_priema": self.data_priema,
            "stazh_let": self.stazh_let()
        }

    def __repr__(self):
        return f"{self.imya} | {self.otdel} | {self.dolzhnost} | {self.zarplata} руб."

# Модуль парсинга CSV — читает файл с данными сотрудников
# Ожидаемые колонки: имя, отдел, должность, зарплата, дата_приема

import csv
import os

ФАЙЛ_ДАННЫХ = "sotrudniki.csv"  # входной файл с данными


class ParsерCSV:
    def __init__(self, filepath=ФАЙЛ_ДАННЫХ):
        self.filepath = filepath

    def proverit_fayl(self):
        # проверяем что файл существует и не пустой
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")
        if os.path.getsize(self.filepath) == 0:
            raise ValueError("Файл пустой")

    def zagruzit(self):
        self.proverit_fayl()
        sotrudniki = []

        with open(self.filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for nomer, stroka in enumerate(reader, start=1):
                try:
                    s = Sotrudnik(
                        imya=stroka["имя"].strip(),
                        otdel=stroka["отдел"].strip(),
                        dolzhnost=stroka["должность"].strip(),
                        zarplata=stroka["зарплата"],
                        data_priema=stroka["дата_приема"].strip()
                    )
                    sotrudniki.append(s)
                except KeyError as e:
                    print(f"! Строка {nomer}: отсутствует колонка {e}, пропускаем")
                except ValueError as e:
                    print(f"! Строка {nomer}: ошибка данных — {e}, пропускаем")

        return sotrudniki