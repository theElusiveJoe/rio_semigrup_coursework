from __future__ import annotations
from .event import Event


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
    events: dict[str, float]

    def __init__(self) -> None:
        self.events = {
            str(Event.check_call): 0,
            str(Event.sg_mult): 0,
        }

    def reset(self):
        self.events = {
            str(Event.check_call): 0,
            str(Event.sg_mult): 0,
        }

    def handle_event(self, e: Event):
        self.events[str(e)] += 1

    def process_events(self) -> dict[str, float]:
        return self.events


EH: EventHandler = EventHandler()
