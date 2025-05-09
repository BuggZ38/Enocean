import requests as rq

class ApiSender:
    def __init__(self, base_url):
        self.__base_url = base_url

    def send(self, data):
        rq.post(f"{self.__base_url}/data", json=data)