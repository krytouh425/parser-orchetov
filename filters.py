# Модуль фильтрации сотрудников — выборки по разным критериям
# Используется для формирования целевых отчётов по запросу HR

class FiltrSotrudnikov:
    def __init__(self, sotrudniki):
        self.sotrudniki = sotrudniki

    def po_otdelu(self, otdel):
        # фильтруем по названию отдела
        return [s for s in self.sotrudniki if s.otdel == otdel]

    def po_zarplate(self, min_zarplata=None, max_zarplata=None):
        # фильтруем по диапазону зарплат
        rezultat = self.sotrudniki
        if min_zarplata:
            rezultat = [s for s in rezultat if s.zarplata >= min_zarplata]
        if max_zarplata:
            rezultat = [s for s in rezultat if s.zarplata <= max_zarplata]
        return rezultat

    def po_stazhu(self, min_let=None, max_let=None):
        # фильтруем по стажу работы
        rezultat = self.sotrudniki
        if min_let:
            rezultat = [s for s in rezultat if s.stazh_let() >= min_let]
        if max_let:
            rezultat = [s for s in rezultat if s.stazh_let() <= max_let]
        return rezultat

    def po_dolzhnosti(self, dolzhnost):
        # фильтруем по должности (частичное совпадение)
        dolzhnost = dolzhnost.lower()
        return [s for s in self.sotrudniki if dolzhnost in s.dolzhnost.lower()]

    def novye_sotrudniki(self, mesyatsev=3):
        # сотрудники принятые за последние N месяцев
        from datetime import datetime
        rezultat = []
        for s in self.sotrudniki:
            try:
                data = datetime.strptime(s.data_priema, "%Y-%m-%d")
                raznitsa = (datetime.now() - data).days / 30
                if raznitsa <= mesyatsev:
                    rezultat.append(s)
            except ValueError:
                continue
        return rezultat

    def vyvesti(self, sotrudniki, zagolovok="РЕЗУЛЬТАТЫ ФИЛЬТРАЦИИ"):
        if not sotrudniki:
            print("Сотрудников по заданным критериям не найдено")
            return

        print(f"\n{'=' * 50}")
        print(f"  {zagolovok}")
        print(f"  Найдено: {len(sotrudniki)} сотрудников")
        print(f"{'=' * 50}")
        for s in sotrudniki:
            print(f"  {s.imya} | {s.otdel} | {s.dolzhnost} | {s.zarplata:,.0f} руб.")
        print(f"{'=' * 50}\n")