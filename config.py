# Конфигурация парсера — все настройки в одном месте
# Меняй здесь не трогая основной код парсера

# настройки входного файла
FAYL_DANNYKH = "sotrudniki.csv"
KODIROVKA = "utf-8"

# настройки валидации
MIN_ZARPLATA = 10000
MAKS_ZARPLATA = 1000000
MAKS_DLINA_IMENI = 100

# настройки отчётов
REPORT_DIR = "reports"
EXPORT_DIR = "exports"
ARCHIVE_DIR = "archive"

# настройки уведомлений
NOVYE_SOTRUDNIKI_DNEY = 30    # считаем новыми если приняты за N дней
VYSOKAYA_ZARPLATA_POROG = 200000  # порог высокой зарплаты
DOLGOSLUZHASHIE_LET = 10      # порог стажа для долгослужащих

# колонки CSV файла
KOLONKI_CSV = {
    "imya": "имя",
    "otdel": "отдел",
    "dolzhnost": "должность",
    "zarplata": "зарплата",
    "data_priema": "дата_приема"
}

# допустимые форматы файлов
FORMATY_IMPORTA = (".csv", ".json")
FORMATY_EXPORTA = ("csv", "json", "txt")