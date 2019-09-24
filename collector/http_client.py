import requests

class HTTPClient :
    def __init__(self, config):
        self.config = config
        self.id = None

    def register(self):
        registration_info =  {"device":"my_mac", "name":"fred", "description":"A test"}
        response = requests.post(self.config["server_url_registration"], registration_info)
        if response.status_code == 200:
            result = response.json()
            self.id = result["id"]
            return True
        else:
            # TODO log failure
            return False

    def send_heart_rate(self, results):
        http_data = results.copy()
        http_data.update({"DeviceId":self.id})
        for key, value in results["trackers"].items():
            http_data.update({key: value})
        response = requests.post(self.config["server_url_heart_rate"], http_data)
        if response.status_code == 200:
            return True
        else:
            # TODO log failure
            return False
