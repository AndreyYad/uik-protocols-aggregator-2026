from get_requests.get_requests import Requests
from uik_info.uiks import Uiks
from excel_file.table import Table
import re

class Main:
    def __init__(self):
        list_error_district = []

        print(
            'Введите какой(ие) округ(а) вам нужны\n',
            'В формате:\n',
            'Пример одного округа: 1\n',
            'Пример нескольких 3-7\n'
        )

        while True:
            enter = input('Ввод: ')
            if re.fullmatch('\d+', enter) and 0 < int(enter) <= 225:
                list_districts_num = [int(enter)]
                break
            if re.fullmatch('\d+-\d+', enter):
                num1, num2 = [int(num_str) for num_str in re.split('-', enter)]
                if not(0 < num1 <= 225 and 0 < num2 <= 225):
                    print('Всего 225 округов - поэтому число должно ыть в иапозоне от 1 до 225')
                elif num1 >= num2:
                    print('Первое число должно быть меньше второго')
                else:
                    list_districts_num = range(num1, num2 + 1)
                    break

        for district in list_districts_num:
            print(f"Генерация таблицы по {district} округу")
            if self.bornDistrictTable(district):
                print(f"Генерация таблицы по {district} округу прошла успешно")
            else:
                list_error_district.append(district)
                print(f"Генерация таблицы по {district} округу не прошла успешно")
            print()
        print(list_error_district)

    def bornDistrictTable(self, district: int=209):
        request = Requests.getDistrictData(district)
        request_fed = Requests.getDistrictData(district, 'fed')
        result = False

        if request_fed is not None and request is not None:
            table = Table(district)

            table.setUiks(Uiks(request))

            table.paint()

            table.createList("Партии")
            table.setUiks(Uiks(request_fed))
            table.paint()

            table.dump()

            result = True

        return result

if __name__ == "__main__":
    Main()