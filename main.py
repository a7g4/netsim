from simulation import Simulation
from events import Event, DatagramEvent, SimulatedNic, EventSink


def main():
    s = Simulation()
    sink = EventSink()
    nic1 = SimulatedNic("eth0_host1", sink, sink)
    nic2 = SimulatedNic("eth0_host2", sink, sink)
    s.add_event(DatagramEvent(0, [nic1], nic2, "asdf"))
    s.add_event(Event(10, [nic1]))
    s.add_event(Event(5, [nic1]))
    s.process_events()
    print(s.pending_events)
    print(s.completed_events)


if __name__ == "__main__":
    main()
