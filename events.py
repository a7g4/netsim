from abc import ABC, abstractmethod
from dataclasses import dataclass
from copy import copy
from typing import List


class Event(object):
    def __init__(self, t: int, processors: List["EventProcessor"]):
        self.t = t
        self.processors = processors

    def __repr__(self) -> str:
        return f'{{"t":{self.t}}}'

    def __lt__(self, other) -> bool:
        return self.t < other.t


class EventProcessor(ABC):
    @abstractmethod
    def process(self, event: Event) -> List[Event]:
        pass

class EventSink(EventProcessor):
    def process(self, event: Event) -> List[Event]:
        return []

class DatagramEvent(Event):
    def __init__(self, t: int, processors: List[EventProcessor], destination, id):
        super().__init__(t, processors)
        self.destination = destination
        self.id = id

    def __repr__(self) -> str:
        return f'{{"t":{self.t}, "id":{self.id}}}'

    def __lt__(self, other) -> bool:
        return super().__lt__(other) and self.id < other.id

class DatagramOnChannelEvent(DatagramEvent):
    def __init__(self, t: int, processors: List[EventProcessor], destination, id):
        super().__init__(t, processors, destination, id)


class DatagramOffChannelEvent(Event):
    def __init__(self, t: int, processors: List[EventProcessor], destination, id):
        super().__init__(t, processors, destination, id)

class SimulatedNic(EventProcessor):
    def __init__(self, name: str, tx_channel: "SimulatedChannel", application):
        super().__init__()
        self.name = name
        self.tx_channel = tx_channel
        self.application = application

    def process(self, event: Event) -> List[Event]:
        match event:
            case DatagramEvent():
                # The application wants to send a datagram onto the channel
                new_event = DatagramOnChannelEvent(event.t + 10, [self.tx_channel], event.destination, event.id)
                return [new_event]
            case DatagramOffChannelEvent():
                # Received a datagram from the channel to send to the application
                if event.destination is self:
                    new_event = DatagramEvent(event.t + 10, [self.application], event.id)
                    return [new_event]
                else:
                    print("{} got an event that wasn't addressed to it: {}".format(self.name, event))
                    return []
            case _:
                # Unknown event
                return []

class SimulatedChannel(EventProcessor):
    def __init__(self, name: str, max_events_in_flight: int, latency: int):
        self.name = name
        self.max_events_in_flight = max_events_in_flight
        self.latency = latency
        self.in_flight = []
    
    def process(self, event: Event):
        match event:
            case DatagramOnChannelEvent():
                # A NIC has put the datagram on this channel
                new_event = DatagramOffChannelEvent(event.t + 10, [self], event.id)
                return [new_event]
            case DatagramOffChannelEvent():
                # The datagram has transitted the channel
                new_event = DatagramEvent(event.t + 10, [self.application], event.id)
            case _:
                # Unknown event
                pass

