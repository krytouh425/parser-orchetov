# Генератор текстовых отчётов — формируем файл для отправки руководству
# Используется после парсинга CSV с данными сотрудников

import os
from datetime import datetime

REPORT_DIR = "reports"  # папка для сохранения отчётов


class ReporterTXT:
    def __init__(self, sotrudniki, report_dir=REPORT_DIR):
        self.sotrudniki = sotrudniki
        self.report_dir = report_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def _imya_fayla(self):
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.report_dir, f"otchet_{vremya}.txt")

    def _shapka(self, f):
        # шапка отчёта с датой и общей статистикой
        f.write("=" * 55 + "\n")
        f.write("  ОТЧЁТ ПО СОТРУДНИКАМ\n")
        f.write(f"  Сформирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"  Всего сотрудников: {len(self.sotrudniki)}\n")
        f.write("=" * 55 + "\n\n")

    def _blok_otdela(self, f, otdel, spisok):
        # блок с данными одного отдела
        zarplaty = [s.zarplata for s in spisok]
        srednyaya = sum(zarplaty) / len(zarplaty)

        f.write(f"[ {otdel.upper()} ]\n")
        f.write(f"  Сотрудников: {len(spisok)}\n")
        f.write(f"  Средняя зарплата: {srednyaya:,.0f} руб.\n")
        f.write(f"  Максимальная: {max(zarplaty):,.0f} руб.\n\n")

        for s in sorted(spisok, key=lambda x: x.zarplata, reverse=True):
            f.write(f"  • {s.imya}\n")
            f.write(f"    Должность: {s.dolzhnost}\n")
            f.write(f"    Зарплата:  {s.zarplata:,.0f} руб.\n")
            f.write(f"    Стаж:      {s.stazh_let()} лет\n\n")

    def sozdat_otchet(self):
        # группируем по отделам и пишем отчёт
        otdely = {}
        for s in self.sotrudniki:
            if s.otdel not in otdely:
                otdely[s.otdel] = []
            otdely[s.otdel].append(s)

        fayl = self._imya_fayla()
        with open(fayl, "w", encoding="utf-8") as f:
            self._shapka(f)
            for otdel in sorted(otdely.keys()):
                self._blok_otdela(f, otdel, otdely[otdel])
            f.write("=" * 55 + "\n")

        print(f"✓ Отчёт сохранён: {fayl}")
        return fayl