import json
import requests


class Requests:

    @staticmethod
    def getDistrictData(districtId: int):
        regionId = Requests.getRegionId(districtId)

        url = (
            "https://pub-9b41d66c14bb4c2fa747a03654838e30.r2.dev"
            f"/data/mand/r{regionId}.json"
        )

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        response = response.json()

        district_uiks = []
        region_uiks = response["uiks"]

        for uik in region_uiks:
            if uik["district"] == districtId:
                district_uiks.append(uik)

        return district_uiks

    @staticmethod
    def getRegionId(districtId: int):
        regions = json.load(open("get_requests/region_districts.json"))
        for regionId in regions.keys():
            if districtId in regions[regionId]:
                return int(regionId)
        return None

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