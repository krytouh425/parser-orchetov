# Модуль статистики — считаем показатели по всем сотрудникам
# Используется для ежемесячных отчётов HR-отдела

class StatistikaSotrudnikov:
    def __init__(self, sotrudniki):
        self.sotrudniki = sotrudniki

    def srednyaya_zarplata(self):
        if not self.sotrudniki:
            return 0
        return sum(s.zarplata for s in self.sotrudniki) / len(self.sotrudniki)

    def mediana_zarplaty(self):
        # медиана точнее средней при больших выбросах
        if not self.sotrudniki:
            return 0
        otsortirovannye = sorted(s.zarplata for s in self.sotrudniki)
        n = len(otsortirovannye)
        if n % 2 == 0:
            return (otsortirovannye[n//2 - 1] + otsortirovannye[n//2]) / 2
        return otsortirovannye[n//2]

    def raspredelenie_po_stazhu(self):
        # группируем сотрудников по стажу
        gruppy = {"до 1 года": [], "1-3 года": [], "3-5 лет": [], "более 5 лет": []}
        for s in self.sotrudniki:
            stazh = s.stazh_let()
            if stazh < 1:
                gruppy["до 1 года"].append(s)
            elif stazh < 3:
                gruppy["1-3 года"].append(s)
            elif stazh < 5:
                gruppy["3-5 лет"].append(s)
            else:
                gruppy["более 5 лет"].append(s)
        return gruppy

    def vyvesti_statistiku(self):
        print("\n" + "=" * 50)
        print("  ОБЩАЯ СТАТИСТИКА")
        print("=" * 50)
        print(f"  Всего сотрудников:   {len(self.sotrudniki)}")
        print(f"  Средняя зарплата:    {self.srednyaya_zarplata():,.0f} руб.")
        print(f"  Медиана зарплат:     {self.mediana_zarplaty():,.0f} руб.")

        print("\n  По стажу:")
        for gruppa, spisok in self.raspredelenie_po_stazhu().items():
            print(f"    {gruppa}: {len(spisok)} чел.")
        print("=" * 50 + "\n")