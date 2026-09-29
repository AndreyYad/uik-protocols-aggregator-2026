from get_requests.get_requests import Requests
from uik_info.uiks import Uiks
from excel_file.table import Table
import re

class Main:
    def __init__(self):
        list_error_district = []

        print(
            "Введите какой(ие) округ(а) вам нужны\n",
            "В формате:\n",
            "Пример одного округа: 1\n",
            "Пример нескольких 3-7\n"
        )

        while True:
            enter = input("Ввод: ")
            if re.fullmatch(r"\d+", enter) and 0 < int(enter) <= 225:
                list_districts_num = [int(enter)]
                break
            if re.fullmatch(r"\d+-\d+", enter):
                num1, num2 = [int(num_str) for num_str in re.split("-", enter)]
                if not(0 < num1 <= 225 and 0 < num2 <= 225):
                    print("Всего 225 округов - поэтому число должно ыть в иапозоне от 1 до 225")
                elif num1 >= num2:
                    print("Первое число должно быть меньше второго")
                else:
                    list_districts_num = range(num1, num2 + 1)
                    break

        for district in list_districts_num:
            print(f"Генерация таблицы по {district} округу")
            if Main.born_district_table(district):
                print(f"Генерация таблицы по {district} округу прошла успешно")
            else:
                list_error_district.append(district)
                print(f"Генерация таблицы по {district} округу не прошла успешно")
            print()
        print(f"Округа, которые не удалось обработать: {list_error_district}")

    @staticmethod
    def born_district_table(district: int=209):
        request = Requests.get_district_data(district)
        request_fed = Requests.get_district_data(district, "fed")
        result = False

        if request_fed is not None and request is not None:
            uiks = Uiks(request)
            uiks_fed = Uiks(request_fed)

            table = Table(district)

            table.set_uiks(uiks)
            table.paint()

            table.create_sheet("Партии")
            table.set_uiks(uiks_fed)
            table.paint()

            table.create_sheet("Одномандатники (%)")
            table.set_uiks(uiks)
            table.paint(percent=True)

            table.create_sheet("Партии (%)")
            table.set_uiks(uiks_fed)
            table.paint(percent=True)

            table.dump()

            result = True

        return result

if __name__ == "__main__":
    Main()