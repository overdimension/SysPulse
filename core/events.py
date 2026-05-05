import logging

class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def emit(self, event_type, *args, **kwargs):
        if event_type not in self._listeners:
            return 

        for listener in self._listeners[event_type]:
            try:
                listener(*args, **kwargs)
            except Exception as e:
                print(f"[EventEmitter Error] Listener {listener.__name__} failed: {e}")