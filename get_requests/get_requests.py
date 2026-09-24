import json
import requests


class Requests:

    @staticmethod
    def getDistrictData(districtId: int, type: str="mand"):
        regionId = Requests.getRegionId(districtId)
        if regionId is None:
            return None

        response = Requests.getRegionData(regionId, type)

        district_uiks = []
        region_uiks = response["uiks"]
        district_uiks_num = Requests.getNumUiksDictrict(districtId, regionId)

        for uik in region_uiks:
            if uik["num"] in district_uiks_num:
                district_uiks.append(uik)

        return district_uiks

    @staticmethod
    def getRegionData(regionId: int, type: str="mand"):
        url = (
            "https://pub-9b41d66c14bb4c2fa747a03654838e30.r2.dev"
            f"/data/{type}/r{regionId}.json"
        )
        result = None
        while True:
            try:
                response = requests.get(url, timeout=300)
            except requests.exceptions.ConnectionError as e:
                print(e)
            else:
                break
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass
        else:
            result = response.json()
        return result

    @staticmethod
    def getRegionId(districtId: int):
        regions = json.load(open("get_requests/region_districts.json"))
        for regionId in regions.keys():
            if districtId in regions[regionId]:
                return int(regionId)
        return None

    @staticmethod
    def getNumUiksDictrict(districtId: int, regionId: int):
        response = Requests.getRegionData(regionId, 'mand')

        uiks_id = []

        for uik in response["uiks"]:
            if uik["district"] == districtId:
                uiks_id.append(int(uik["num"]))

        return uiks_id

    @staticmethod
    def createRegionDistrictsFile(filename="region_districts.json"):
        result = {}

        for regionId in range(91):
            print(f"Обрабатываю регион {regionId}...")

            try:
                regionData = Requests.getRegionData(regionId)
            except (requests.RequestException, requests.JSONDecodeError) as e:
                print(f"  Ошибка: {e}")
                continue

            districts = {
                uik["district"]
                for uik in regionData.get("uiks", [])
                if "district" in uik
            }

            result[str(regionId)] = sorted(districts)

            print(f"  Найдено округов: {len(districts)}")

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                result,
                file,
                ensure_ascii=False,
                indent=2
            )

        print(f"\nГотово! Файл сохранён: {filename}")

        return result

if __name__ == "__main__":
    Requests.createRegionDistrictsFile()