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

# Генератор отчётов — формирует сводку по отделам
# Считает среднюю зарплату, количество сотрудников, средний стаж

class GeneratorOtchetov:
    def __init__(self, sotrudniki):
        self.sotrudniki = sotrudniki

    def po_otdelam(self):
        # группируем сотрудников по отделам
        otdely = {}
        for s in self.sotrudniki:
            if s.otdel not in otdely:
                otdely[s.otdel] = []
            otdely[s.otdel].append(s)
        return otdely

    def svodka(self):
        otdely = self.po_otdelam()

        print("\n" + "=" * 50)
        print("  ОТЧЁТ ПО ОТДЕЛАМ")
        print("=" * 50)

        for otdel, spisok in sorted(otdely.items()):
            zarplaty = [s.zarplata for s in spisok]
            stazhi = [s.stazh_let() for s in spisok]

            print(f"\n📁 {otdel}")
            print(f"   Сотрудников:      {len(spisok)}")
            print(f"   Средняя зарплата: {sum(zarplaty) / len(zarplaty):,.0f} руб.")
            print(f"   Макс. зарплата:   {max(zarplaty):,.0f} руб.")
            print(f"   Средний стаж:     {sum(stazhi) / len(stazhi):.1f} лет")

        print("\n" + "=" * 50)
        print(f"  Всего сотрудников: {len(self.sotrudniki)}")
        print("=" * 50 + "\n")

    def spisok_otdela(self, otdel):
        # выводим всех сотрудников конкретного отдела
        otdely = self.po_otdelam()
        if otdel not in otdely:
            print(f"Отдел '{otdel}' не найден")
            return

        print(f"\n{'=' * 50}")
        print(f"  СОТРУДНИКИ ОТДЕЛА: {otdel}")
        print(f"{'=' * 50}")
        for s in otdely[otdel]:
            print(f"  {s.imya} | {s.dolzhnost} | {s.zarplata:,.0f} руб. | стаж {s.stazh_let()} лет")
        print(f"{'=' * 50}\n")

# Валидация данных — проверяем корректность перед обработкой
# Защищаем систему от кривых данных в CSV

from datetime import datetime

ДОПУСТИМЫЕ_ОТДЕЛЫ = ("HR", "IT", "Бухгалтерия", "Продажи", "Логистика", "Маркетинг")
МИНИМАЛЬНАЯ_ЗАРПЛАТА = 10000
МАКСИМАЛЬНАЯ_ЗАРПЛАТА = 1000000


def валидировать_зарплату(zarplata):
    try:
        z = float(zarplata)
    except ValueError:
        raise ValueError(f"Зарплата должна быть числом, получено: '{zarplata}'")

    if z < МИНИМАЛЬНАЯ_ЗАРПЛАТА:
        raise ValueError(f"Зарплата {z} ниже минимальной ({МИНИМАЛЬНАЯ_ЗАРПЛАТА})")
    if z > МАКСИМАЛЬНАЯ_ЗАРПЛАТА:
        raise ValueError(f"Зарплата {z} выше максимальной ({МАКСИМАЛЬНАЯ_ЗАРПЛАТА})")
    return z


def валидировать_дату(data):
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Неверный формат даты '{data}', ожидается ГГГГ-ММ-ДД")
    return data


def валидировать_имя(imya):
    imya = imya.strip()
    if not imya:
        raise ValueError("Имя сотрудника не может быть пустым")
    if len(imya) < 2:
        raise ValueError(f"Имя слишком короткое: '{imya}'")
    if any(c.isdigit() for c in imya):
        raise ValueError(f"Имя не должно содержать цифры: '{imya}'")
    return imya


def запустить_парсер(filepath=None):
    # точка входа — загружаем данные и выводим отчёт
    parser = ParsерCSV(filepath) if filepath else ParsерCSV()

    try:
        sotrudniki = parser.zagruzit()
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return
    except ValueError as e:
        print(f"Ошибка файла: {e}")
        return

    if not sotrudniki:
        print("Нет данных для построения отчёта")
        return

    otchet = GeneratorOtchetov(sotrudniki)
    otchet.svodka()


if __name__ == "__main__":
    запустить_парсер()

# вспомогательная функция — выводим топ сотрудников по зарплате
# добавлено для быстрого просмотра на совещаниях

def top_po_zarplate(sotrudniki, kolichestvo=5):
    otsortirovannye = sorted(sotrudniki, key=lambda s: s.zarplata, reverse=True)
    return otsortirovannye[:kolichestvo]