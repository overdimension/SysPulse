from abc import ABC, abstractmethod

#Interface
class HttpClient(ABC):
    @abstractmethod
    def send_request(self, url: str, method: str = "GET", data: dict = None):
        pass

#Basic implementation of HttpClient
class BaseHttpClient(HttpClient):
    def send_request(self, url: str, method: str = "GET", data: dict = None):
        print(f"[BaseClient] Sending {method} request to {url}...")
        return {"status": 200, "body": "Success"}

class AuthProxy(HttpClient):
    def __init__(self, real_client: HttpClient, api_key: str):
        self._real_client = real_client 
        self._api_key = api_key

    def send_request(self, url: str, method: str = "GET", data: dict = None):
        print("[AuthProxy] Injecting API Key into headers...")
        #AuthProxy
        headers = {"Authorization": f"Bearer {self._api_key}"}
        return self._real_client.send_request(url, method, data)

class CloudExporter:
    def __init__(self, client: HttpClient): #DI
        self.client = client

    def export_data(self, data):
        url = "https://api.syspulse.com/v1/metrics"
        return self.client.send_request(url, method="POST", data=data)