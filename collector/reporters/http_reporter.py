import requests
import socket
from utilities import get_machine_id

class HTTPReporter :
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.id = None

    def report_results(self, results):
        if results["passCount"] == 1:
            self.register(results["video_name"])

        self.send_heart_rate(results)

    def register(self, video_name):
        registration_info = {"device":get_machine_id(), "video":video_name}
        try:
            if "computer_name" in self.config:
                registration_info.update({"name":socket.gethostname()})
            if "computer_description" in self.config:
                registration_info.update({"description": self.config["computer_description"]})
            response = requests.post("{}{}".format(self.config["server_url"], "register"), registration_info)
            if response.status_code == 200:
                result = response.json()
                self.id = result["id"]
                return True
            else:
                self.logger.error("Registration failure, HTTP status: {}".format(response.status_code))
                return False
        except requests.exceptions.RequestException as err:
            self.logger.error("Exception: {}".format(err))

    def send_heart_rate(self, results):
        try:
            http_data = results.copy()
            http_data.update({"DeviceId":self.id})
            for key, value in results["trackers"].items():
                http_data.update({key: value})
            response = requests.post("{}{}".format(self.config["server_url"], "heartrate"), http_data)
            if response.status_code == 200:
                return True
            else:
                self.logger.error("POST failure, HTTP status: {}".format(response.status_code))
                return False

        except requests.exceptions.RequestException as err:
            self.logger.error("Exception: {}".format(err))
