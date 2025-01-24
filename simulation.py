import heapq
from events import Event

class Simulation(object):
    def __init__(self):
        self.simulation_time = 0
        self.pending_events = []
        self.completed_events = []

    def add_event(self, event: Event):
        heapq.heappush(self.pending_events, event)

    def process_events(self):
        while len(self.pending_events) > 0:
            next_event = heapq.heappop(self.pending_events)
            if next_event.t < self.simulation_time:
                raise "Something went wrong"
            else:
                self.simulation_time = next_event.t
            new_events = []
            for processor in next_event.processors:
                [new_events.append(new_event) for new_event in processor.process(next_event)]
            [self.add_event(e) for e in new_events]
            self.completed_events.append(next_event)
