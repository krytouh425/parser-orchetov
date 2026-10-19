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