# Модуль планировщика — запускаем парсинг по расписанию
# Используется для автоматического обновления отчётов HR-отдела

import time
from datetime import datetime


class PlanirovshhikParsinga:
    def __init__(self, filepath=None, interval_minut=60):
        self.filepath = filepath
        self.interval = interval_minut * 60  # переводим в секунды
        self.istoriya = []  # история запусков

    def _zapisat_rezultat(self, kolichestvo, uspeshno):
        self.istoriya.append({
            "vremya": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kolichestvo": kolichestvo,
            "uspeshno": uspeshno
        })

    def odin_zapusk(self):
        # запускаем один цикл парсинга
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Запуск парсинга...")
        try:
            from parser import ParsерCSV, GeneratorOtchetov
            parser = ParsерCSV(self.filepath) if self.filepath else ParsерCSV()
            sotrudniki = parser.zagruzit()
            otchet = GeneratorOtchetov(sotrudniki)
            otchet.svodka()
            self._zapisat_rezultat(len(sotrudniki), True)
            print(f"✓ Парсинг завершён — обработано {len(sotrudniki)} сотрудников")
            return True
        except Exception as e:
            print(f"✗ Ошибка парсинга: {e}")
            self._zapisat_rezultat(0, False)
            return False

    def pokazat_istoriyu(self):
        if not self.istoriya:
            print("История запусков пуста")
            return

        uspeshno = len([z for z in self.istoriya if z["uspeshno"]])
        print(f"\n{'=' * 45}")
        print(f"  ИСТОРИЯ ЗАПУСКОВ ({len(self.istoriya)} всего)")
        print(f"  Успешно: {uspeshno} | Ошибок: {len(self.istoriya) - uspeshno}")
        print(f"{'=' * 45}")
        for z in self.istoriya[-10:]:
            status = "✓" if z["uspeshno"] else "✗"
            print(f"  [{status}] {z['vremya']} — {z['kolichestvo']} сотрудников")
        print(f"{'=' * 45}\n")

    def zapustit_v_rezhime_avtomata(self, max_zapuskov=None):
        zapuskov = 0
        print(f"Автопарсинг запущен. Интервал: {self.interval // 60} мин.")
        print("Для остановки нажмите Ctrl+C\n")

        try:
            while True:
                self.odin_zapusk()
                zapuskov += 1
                if max_zapuskov and zapuskov >= max_zapuskov:
                    break
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nАвтопарсинг остановлен")

        self.pokazat_istoriyu()