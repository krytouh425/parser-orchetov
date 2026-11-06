# Модуль архивации отчётов — сохраняем историю данных по сотрудникам
# Используется для хранения ежемесячных снимков данных HR

import json
import os
from datetime import datetime

ARCHIVE_DIR = "archive"  # папка для архивов


class ArkhivOtchetov:
    def __init__(self, archive_dir=ARCHIVE_DIR):
        self.archive_dir = archive_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def _imya_fayla(self):
        vremya = datetime.now().strftime("%Y%m")
        return os.path.join(self.archive_dir, f"otchet_{vremya}.json")

    def sohranit_snapshot(self, sotrudniki):
        # сохраняем текущее состояние данных
        danye = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kolichestvo": len(sotrudniki),
            "sotrudniki": [s.to_dict() for s in sotrudniki]
        }
        fayl = self._imya_fayla()
        with open(fayl, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)
        print(f"✓ Снимок данных сохранён: {fayl}")
        return fayl

    def zagruzit_snapshot(self, god, mesyats):
        # загружаем архивный снимок за указанный месяц
        fayl = os.path.join(self.archive_dir, f"otchet_{god}{mesyats:02d}.json")
        if not os.path.exists(fayl):
            raise FileNotFoundError(f"Архив за {mesyats}/{god} не найден")
        with open(fayl, encoding="utf-8") as f:
            return json.load(f)

    def spisok_arkhivov(self):
        fayly = sorted([
            f for f in os.listdir(self.archive_dir)
            if f.startswith("otchet_") and f.endswith(".json")
        ], reverse=True)

        if not fayly:
            print("Архивов нет")
            return []

        print(f"\n{'=' * 40}")
        print(f"  АРХИВЫ ОТЧЁТОВ ({len(fayly)})")
        print(f"{'=' * 40}")
        for f in fayly:
            put = os.path.join(self.archive_dir, f)
            razmer = os.path.getsize(put) / 1024
            print(f"  {f} ({razmer:.1f} КБ)")
        print(f"{'=' * 40}\n")
        return fayly