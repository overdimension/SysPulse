from abc import ABC, abstractmethod
import datetime

class BaseCollector(ABC):
    def __init__(self):
        self.name = self.__class__.__name__.replace('Collector', '').lower()


    @abstractmethod
    def collect(self) -> dict:
        """
        Реализация сбора данных в дочерних классах
        """
        pass


    def get_data(self) -> dict:
        """
        Метод для получения данных с добавлением временной метки
        """
        try:
            return {
                "timestamp": datetime.datetime.now().isoformat(),
                "collector": self.name,
                "status": "success",
                "metrics": self.collect()
            }
        except Exception as e:
            return {
                "timestamp": datetime.datetime.now().isoformat(),
                "collector": self.name,
                "status": "error",
                "error_message": str(e)
            }