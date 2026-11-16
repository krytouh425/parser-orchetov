# Модуль сводки — формируем краткий дайджест для руководства
# Используется еженедельно для отчёта перед директором

from datetime import datetime


class SvodkaRukovodstva:
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

    def klyuchevye_pokazateli(self):
        otdely = self._otdely()
        zarplaty = [s.zarplata for s in self.sotrudniki]

        return {
            "vsego_sotrudnikov": len(self.sotrudniki),
            "vsego_otdelov": len(otdely),
            "srednyaya_zarplata": sum(zarplaty) / len(zarplaty) if zarplaty else 0,
            "maks_zarplata": max(zarplaty) if zarplaty else 0,
            "min_zarplata": min(zarplaty) if zarplaty else 0,
            "sredний_stazh": sum(s.stazh_let() for s in self.sotrudniki) / len(self.sotrudniki) if self.sotrudniki else 0
        }

    def vyvesti(self):
        pokazateli = self.klyuchevye_pokazateli()
        otdely = self._otdely()

        print(f"\n{'=' * 55}")
        print(f"  СВОДКА ДЛЯ РУКОВОДСТВА")
        print(f"  Дата: {self.vremya.strftime('%d.%m.%Y')}")
        print(f"{'=' * 55}")
        print(f"  Сотрудников всего:   {pokazateli['vsego_sotrudnikov']}")
        print(f"  Отделов:             {pokazateli['vsego_otdelov']}")
        print(f"  Средняя зарплата:    {pokazateli['srednyaya_zarplata']:,.0f} руб.")
        print(f"  Максимальная:        {pokazateli['maks_zarplata']:,.0f} руб.")
        print(f"  Средний стаж:        {pokazateli['sredний_stazh']:.1f} лет")
        print(f"\n  По отделам:")
        for otdel, spisok in sorted(otdely.items()):
            srednyaya = sum(s.zarplata for s in spisok) / len(spisok)
            print(f"    {otdel}: {len(spisok)} чел. | ср. {srednyaya:,.0f} руб.")
        print(f"{'=' * 55}\n")