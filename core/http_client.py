from abc import ABC, abstractmethod

#Interface
class HttpClient(ABC):
    @abstractmethod
    def send_request(self, url: str, method: str = "GET", data: dict = None):
        pass

#Basic implementation of HttpClient
class BaseHttpClient(HttpClient):
    def send_request(self, url: str, method: str = "GET", data: dict = None):
        print(f"[BaseClient] Відправка {method} запиту на {url}...")
        return {"status": 200, "body": "Success"}