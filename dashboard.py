# Дашборд HR — главный экран с ключевыми показателями
# Выводится при запуске парсера как сводный отчёт

from datetime import datetime


class DashboardHR:
    def __init__(self, sotrudniki):
        self.sotrudniki = sotrudniki
        self.vremya = datetime.now()

    def _otdely(self):
        otdely = {}
        for s in self.sotrudniki:
            if s.otdel not in otdely:
                otdely[s.otdel] = []
            otdely[s.otdel].append(s)
        return otdely

    def _novye(self, dney=30):
        novye = []
        for s in self.sotrudniki:
            try:
                data = datetime.strptime(s.data_priema, "%Y-%m-%d")
                if (self.vremya - data).days <= dney:
                    novye.append(s)
            except ValueError:
                continue
        return novye

    def pokazat(self):
        otdely = self._otdely()
        novye = self._novye()
        zarplaty = [s.zarplata for s in self.sotrudniki]
        srednyaya = sum(zarplaty) / len(zarplaty) if zarplaty else 0
        sredний_stazh = sum(s.stazh_let() for s in self.sotrudniki) / len(self.sotrudniki) if self.sotrudniki else 0

        print(f"\n{'=' * 55}")
        print(f"  HR ДАШБОРД — {self.vremya.strftime('%d.%m.%Y %H:%M')}")
        print(f"{'=' * 55}")
        print(f"  Сотрудников:         {len(self.sotrudniki)}")
        print(f"  Отделов:             {len(otdely)}")
        print(f"  Средняя зарплата:    {srednyaya:,.0f} руб.")
        print(f"  Средний стаж:        {sredний_stazh:.1f} лет")
        print(f"  Новые (до 30 дней):  {len(novye)}")

        print(f"\n  Топ отделов по численности:")
        for otdel, spisok in sorted(otdely.items(), key=lambda x: len(x[1]), reverse=True)[:3]:
            print(f"    {otdel}: {len(spisok)} чел.")

        if novye:
            print(f"\n  Новые сотрудники:")
            for s in novye[:3]:
                print(f"    {s.imya} — {s.otdel}")

        print(f"{'=' * 55}\n")