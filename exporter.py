# Модуль экспорта — выгружаем данные сотрудников в разные форматы
# Используется HR-отделом для передачи данных в другие системы

import csv
import json
import os
from datetime import datetime

EXPORT_DIR = "exports"


class ExporterSotrudnikov:
    def __init__(self, sotrudniki, export_dir=EXPORT_DIR):
        self.sotrudniki = sotrudniki
        self.export_dir = export_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def _imya_fayla(self, format):
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.export_dir, f"sotrudniki_{vremya}.{format}")

    def v_csv(self):
        fayl = self._imya_fayla("csv")
        with open(fayl, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Имя", "Отдел", "Должность", "Зарплата", "Стаж"])
            for s in self.sotrudniki:
                writer.writerow([
                    s.imya, s.otdel, s.dolzhnost,
                    s.zarplata, s.stazh_let()
                ])
        print(f"✓ Экспортировано в CSV: {fayl}")
        return fayl

    def v_json(self):
        fayl = self._imya_fayla("json")
        with open(fayl, "w", encoding="utf-8") as f:
            json.dump(
                [s.to_dict() for s in self.sotrudniki],
                f, ensure_ascii=False, indent=2
            )
        print(f"✓ Экспортировано в JSON: {fayl}")
        return fayl

    def top_zarplat(self, kolichestvo=10):
        # экспортируем топ сотрудников по зарплате
        fayl = self._imya_fayla("txt")
        top = sorted(self.sotrudniki, key=lambda s: s.zarplata, reverse=True)[:kolichestvo]
        with open(fayl, "w", encoding="utf-8") as f:
            f.write(f"ТОП-{kolichestvo} ПО ЗАРПЛАТЕ\n")
            f.write("=" * 45 + "\n\n")
            for i, s in enumerate(top, 1):
                f.write(f"{i}. {s.imya} — {s.zarplata:,.0f} руб.\n")
                f.write(f"   {s.otdel} | {s.dolzhnost}\n\n")
        print(f"✓ Топ зарплат сохранён: {fayl}")
        return fayl