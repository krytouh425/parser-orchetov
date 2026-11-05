# Модуль уведомлений — оповещаем HR о важных изменениях в данных
# Используется после каждого парсинга для информирования команды

from datetime import datetime


class NotifierHR:
    def __init__(self, sotrudniki):
        self.sotrudniki = sotrudniki
        self.vremya = datetime.now()

    def novye_sotrudniki(self, dney=30):
        # сотрудники принятые за последние N дней
        novye = []
        for s in self.sotrudniki:
            try:
                data = datetime.strptime(s.data_priema, "%Y-%m-%d")
                raznitsa = (self.vremya - data).days
                if raznitsa <= dney:
                    novye.append(s)
            except ValueError:
                continue
        return novye

    def vysokie_zarplaty(self, porog=200000):
        # сотрудники с зарплатой выше порога
        return [s for s in self.sotrudniki if s.zarplata >= porog]

    def dolgosluzhashie(self, let=10):
        # сотрудники со стажем больше N лет
        return [s for s in self.sotrudniki if s.stazh_let() >= let]

    def sformirovat_svodku(self):
        novye = self.novye_sotrudniki()
        vysokie = self.vysokie_zarplaty()
        dolgiye = self.dolgosluzhashie()

        print(f"\n{'=' * 50}")
        print(f"  СВОДКА ДЛЯ HR")
        print(f"  Дата: {self.vremya.strftime('%d.%m.%Y %H:%M')}")
        print(f"{'=' * 50}")
        print(f"  Всего сотрудников:     {len(self.sotrudniki)}")
        print(f"  Новые (до 30 дней):    {len(novye)}")
        print(f"  Зарплата > 200к:       {len(vysokie)}")
        print(f"  Стаж > 10 лет:         {len(dolgiye)}")

        if novye:
            print(f"\n  Новые сотрудники:")
            for s in novye:
                print(f"    {s.imya} — {s.otdel} ({s.data_priema})")

        print(f"{'=' * 50}\n")