# Модуль сравнения отчётов — сравниваем данные за разные периоды
# Используется HR для отслеживания динамики зарплат и состава отделов

class SravnitelOtchetov:
    def __init__(self, tekushie, predydushie):
        self.tekushie = tekushie        # текущий список сотрудников
        self.predydushie = predydushie  # предыдущий список сотрудников

    def _po_otdelam(self, sotrudniki):
        # группируем сотрудников по отделам
        otdely = {}
        for s in sotrudniki:
            if s.otdel not in otdely:
                otdely[s.otdel] = []
            otdely[s.otdel].append(s)
        return otdely

    def srednyaya_zarplata(self, sotrudniki):
        if not sotrudniki:
            return 0
        return sum(s.zarplata for s in sotrudniki) / len(sotrudniki)

    def sravnit_otdely(self):
        # сравниваем показатели по каждому отделу
        tekushie_otdely = self._po_otdelam(self.tekushie)
        predydushie_otdely = self._po_otdelam(self.predydushie)

        vse_otdely = set(tekushie_otdely) | set(predydushie_otdely)
        rezultaty = []

        for otdel in sorted(vse_otdely):
            tek = tekushie_otdely.get(otdel, [])
            pred = predydushie_otdely.get(otdel, [])

            tek_zarplata = self.srednyaya_zarplata(tek)
            pred_zarplata = self.srednyaya_zarplata(pred)

            if pred_zarplata > 0:
                izmenenie = ((tek_zarplata - pred_zarplata) / pred_zarplata) * 100
            else:
                izmenenie = 0

            rezultaty.append({
                "otdel": otdel,
                "tek_kolichestvo": len(tek),
                "pred_kolichestvo": len(pred),
                "tek_zarplata": tek_zarplata,
                "pred_zarplata": pred_zarplata,
                "izmenenie_zarplaty": round(izmenenie, 1)
            })

        return rezultaty

    def vyvesti_sravnenie(self):
        rezultaty = self.sravnit_otdely()

        print("\n" + "=" * 55)
        print("  СРАВНЕНИЕ ОТЧЁТОВ ПО ОТДЕЛАМ")
        print("=" * 55)

        for r in rezultaty:
            znak = "+" if r["izmenenie_zarplaty"] >= 0 else ""
            print(f"\n  {r['otdel']}")
            print(f"    Сотрудников: {r['pred_kolichestvo']} → {r['tek_kolichestvo']}")
            print(f"    Средняя зарплата: {r['pred_zarplata']:,.0f} → {r['tek_zarplata']:,.0f} руб.")
            print(f"    Изменение: {znak}{r['izmenenie_zarplaty']}%")

        print("\n" + "=" * 55 + "\n")