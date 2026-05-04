from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def save(self, collector_name: str, metrics: dict):
        """Method for saving data"""
        pass


    @abstractmethod
    def get_all(self):
        """Method for getting all accumulated data"""
        pass