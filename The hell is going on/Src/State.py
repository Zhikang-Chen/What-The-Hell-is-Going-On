from abc import ABC, abstractmethod

#State Base Class
class State(ABC):
    state_change = False;
    next_state = None;

    @abstractmethod
    def display_frame(self):
        pass

    @abstractmethod
    def process_events(self):
        pass

    @abstractmethod
    def run_logic(self):
        pass

    def change_state(self, State):
        self.change_state = True
        self.next_state = State
