from storage.base import BaseStorage
import logging

class MemoryStorage(BaseStorage):
    def __init__(self):
        self._data = []
        logging.info("The memory storage has been initialized.")


    def save(self, collector_name: str, metrics: dict):
        entry = {
            "collector": collector_name,
            "metrics": metrics
        }
        self._data.append(entry)

        if len(self._data) > 1000:
            self._data.pop(0) 


    def get_all(self):
        return self._data