from models import State


class Output:
    def __init__(self, values):
        self.values = values

    def states_capitals_out(self):
        for state_name, state_abr, capital_name in self.values:
            State().add_state(state_name, state_abr)
            state = State().get_state(state_name)
            state.add_state_capital(capital_name)
