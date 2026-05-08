from abc import ABC, abstractmethod
from storage.cloud_storage import CloudStorage

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

class LocalCloudClient(HttpClient):
    """Uses local cloud storage instead of remote server (for development)"""
    def __init__(self):
        self.storage = CloudStorage()
    
    def send_request(self, url: str, method: str = "GET", data: dict = None):
        if method == "POST":
            self.storage.save_metrics(data)
            print("[LocalCloud] 💾 Metrics saved locally")
            return {"status": 200, "body": "Saved to local cloud"}
        elif method == "GET":
            result = self.storage.get_last_metrics(10)
            print("[LocalCloud] 📂 Metrics retrieved from local cloud")
            return {"status": 200, "body": result}
        return {"status": 400, "body": "Unknown method"}

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
    
    def get_data(self):
        """Retrieve metrics from cloud"""
        url = "https://api.syspulse.com/v1/metrics"
        return self.client.send_request(url, method="GET")