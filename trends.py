# Модуль трендов — анализируем динамику изменений данных
# Используется для сравнения показателей за разные периоды

from datetime import datetime


class AnalizTrendov:
    def __init__(self, tekushie, predydushie=None):
        self.tekushie = tekushie
        self.predydushie = predydushie or []

    def _srednyaya_zarplata(self, sotrudniki):
        if not sotrudniki:
            return 0
        return sum(s.zarplata for s in sotrudniki) / len(sotrudniki)

    def _po_otdelam(self, sotrudniki):
        otdely = {}
        for s in sotrudniki:
            if s.otdel not in otdely:
                otdely[s.otdel] = []
            otdely[s.otdel].append(s)
        return otdely

    def dinamika_zarplat(self):
        tek = self._srednyaya_zarplata(self.tekushie)
        pred = self._srednyaya_zarplata(self.predydushie)

        if pred == 0:
            return {"tekushaya": tek, "predydushaya": pred, "izmenenie": 0}

        izmenenie = ((tek - pred) / pred) * 100
        return {
            "tekushaya": tek,
            "predydushaya": pred,
            "izmenenie": round(izmenenie, 1)
        }

    def dinamika_chislennosti(self):
        tek = len(self.tekushie)
        pred = len(self.predydushie)
        raznitsa = tek - pred
        return {
            "tekushaya": tek,
            "predydushaya": pred,
            "raznitsa": raznitsa
        }

    def novye_otdely(self):
        # отделы которые появились в текущем периоде
        tek_otdely = set(self._po_otdelam(self.tekushie).keys())
        pred_otdely = set(self._po_otdelam(self.predydushie).keys())
        return tek_otdely - pred_otdely

    def vyvesti(self):
        zarplaty = self.dinamika_zarplat()
        chislennost = self.dinamika_chislennosti()
        novye = self.novye_otdely()

        print(f"\n{'=' * 50}")
        print(f"  АНАЛИЗ ТРЕНДОВ")
        print(f"{'=' * 50}")

        znak = "+" if zarplaty["izmenenie"] >= 0 else ""
        print(f"  Средняя зарплата:")
        print(f"    Текущая:    {zarplaty['tekushaya']:,.0f} руб.")
        print(f"    Предыдущая: {zarplaty['predydushaya']:,.0f} руб.")
        print(f"    Изменение:  {znak}{zarplaty['izmenenie']}%")

        print(f"\n  Численность:")
        print(f"    Текущая:    {chislennost['tekushaya']} чел.")
        print(f"    Предыдущая: {chislennost['predydushaya']} чел.")
        raznitsa = chislennost['raznitsa']
        print(f"    Изменение:  {'+' if raznitsa >= 0 else ''}{raznitsa} чел.")

        if novye:
            print(f"\n  Новые отделы: {', '.join(novye)}")

        print(f"{'=' * 50}\n")