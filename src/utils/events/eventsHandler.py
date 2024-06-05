from __future__ import annotations
from .event import Event
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


def spawn_event(e: Event):
    EH.handle_event(e)


def event_on_startup(e: Event):
    def decorator(func):
        def wrapper(*args, **kwargs):
            spawn_event(e)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class EventHandler:
    events: list[Event]

    def __init__(self) -> None:
        self.events = []

    @staticmethod
    def reset():
        global EH
        EH = EventHandler()

    def handle_event(self, e: Event):
        logging.info(f'event {e}')
        self.events.append(e)

    def create_report(self):
        print('report:')
        for e in self.events:
            print(e)


EH: EventHandler = EventHandler()
