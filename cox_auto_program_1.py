# Nihjur Yarbrough
# Cox Automotive, Programming Challenge
# 8/1/2021

import requests
import json

def main():
    get_datasetId = requests.get("http://api.coxauto-interview.com/api/datasetId", auth=("user", "pass"))

    if get_datasetId.status_code == 200:
        print("datasetId Success.")
        datasetId = get_datasetId.json().get("datasetId", "")
        if len(datasetId.replace(" ", "")) > 0:
            print("Dataset ID retrieved!")
            print(datasetId)
        else:
            print("No datasetId retrieved.")
            return 0
    else:
        print("datasetId Failed.")
        print(f"Get datasetId failed. Status code {get_datasetId.status_code}.")
        return 0

    dealers = {}
    get_vehicles = requests.get(f"http://api.coxauto-interview.com/api/{datasetId}/vehicles", auth=("user", "pass"))

    if get_vehicles.status_code == 200:
        print("get_vehicles Success.")
        vehicleIds = get_vehicles.json().get("vehicleIds", [])
        if len(vehicleIds) > 0:
            print("Vehicles retrieved!")
            for v in vehicleIds:
                get_v = requests.get(f"http://api.coxauto-interview.com/api/{datasetId}/vehicles/{v}", auth=("user", "pass"))
                if get_v.status_code == 200:
                    v_json = get_v.json()
                    dealerId = v_json.get("dealerId", 0)
                    if dealerId > 0:
                        try:
                            v_json.pop("dealerId", None)
                            dealers[f"{dealerId}"]["vehicles"].append(v_json)
                        except KeyError:
                            print("New Dealer found.")
                            get_dealer = requests.get(f"http://api.coxauto-interview.com/api/{datasetId}/dealers/{dealerId}", auth=("user", "pass"))
                            if get_dealer.status_code == 200:
                                dealer_json = get_dealer.json()
                                if dealer_json.get("dealerId", 0) == dealerId:
                                    v_json.pop("dealerId", None)
                                    dealer_json["vehicles"] = [v_json]
                                    dealers[f"{dealerId}"] = dealer_json
        else:
            print("No vehicle IDs retrieved.")
            return 0
    else:
        print(f"Get vehicles failed. Status code {get_vehicles.status_code}.")
        return 0

    answer = json.dumps({"dealers": list(dealers.values())})
    result = requests.post(
        f"http://api.coxauto-interview.com/api/{datasetId}/answer",
        headers = {"accept": "application/json", "Content-Type": "application/json"},
        data = answer
    )
    print(result.json())
    return 0

if __name__ == "__main__":
    main()
