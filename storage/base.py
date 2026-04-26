from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def save(self, collector_name: str, metrics: dict):
        """Метод для сохранения данных"""
        pass


    @abstractmethod
    def get_all(self):
        """Метод для получения всех накопленных данных"""
        pass