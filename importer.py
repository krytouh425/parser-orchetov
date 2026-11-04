# Модуль импорта — загружаем данные сотрудников из разных форматов
# Используется при миграции данных из старых систем HR

import csv
import json
import os


class ImporterSotrudnikov:
    def __init__(self, filepath):
        self.filepath = filepath

    def _proverit_fayl(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")
        if os.path.getsize(self.filepath) == 0:
            raise ValueError("Файл пустой")

    def iz_csv(self):
        # импортируем из CSV — ожидаем колонки как в основном парсере
        self._proverit_fayl()
        danye = []

        with open(self.filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for nomer, stroka in enumerate(reader, start=1):
                try:
                    danye.append({
                        "imya": stroka["имя"].strip(),
                        "otdel": stroka["отдел"].strip(),
                        "dolzhnost": stroka["должность"].strip(),
                        "zarplata": float(stroka["зарплата"]),
                        "data_priema": stroka["дата_приема"].strip()
                    })
                except KeyError as e:
                    print(f"! Строка {nomer}: нет колонки {e}, пропускаем")
                except ValueError as e:
                    print(f"! Строка {nomer}: ошибка данных {e}, пропускаем")

        print(f"✓ Загружено из CSV: {len(danye)} записей")
        return danye

    def iz_json(self):
        # импортируем из JSON — формат как в экспорте
        self._proverit_fayl()

        with open(self.filepath, encoding="utf-8") as f:
            danye = json.load(f)

        if not isinstance(danye, list):
            raise ValueError("JSON должен содержать список записей")

        print(f"✓ Загружено из JSON: {len(danye)} записей")
        return danye

    def opredelit_format(self):
        # автоматически определяем формат по расширению файла
        _, rasshirenie = os.path.splitext(self.filepath)
        if rasshirenie.lower() == ".csv":
            return self.iz_csv()
        elif rasshirenie.lower() == ".json":
            return self.iz_json()
        else:
            raise ValueError(f"Неподдерживаемый формат: {rasshirenie}")