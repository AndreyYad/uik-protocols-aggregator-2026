from get_requests.get_requests import Requests
from uik_info.uiks import Uiks
from excel_file.table import Table

class Main:
    def __init__(self):
        list_error_district = []
        for district in range(13, 226):
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