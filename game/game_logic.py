import random

class DealOrNoDeal:
    def __init__(self):
        self.cases = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000]
        random.shuffle(self.cases)
        self.selected_case = None
        self.remaining_cases = {i: value for i, value in enumerate(self.cases, start=1)}
        self.opened_cases = []
        self.bank_offers = []
        self.rounds = [6, 5, 4, 3, 2, 1, 1]  # Rondas de selección de maletines
        self.current_round = 0
        self.cases_to_open = self.rounds[self.current_round]  # Maletines a abrir en la ronda actual

    def select_case(self, case_number):
        if self.selected_case is None:
            self.selected_case = self.remaining_cases.pop(case_number)
            return self.selected_case
        else:
            raise ValueError("El maletín principal ya ha sido seleccionado.")

    def open_case(self, case_number):
        if case_number in self.remaining_cases:
            case_value = self.remaining_cases.pop(case_number)
            self.opened_cases.append((case_number, case_value))
            self.cases_to_open -= 1

            if self.cases_to_open == 0:
                self.current_round += 1
                if self.current_round < len(self.rounds):
                    self.cases_to_open = self.rounds[self.current_round]

            return case_value
        else:
            raise ValueError(f"El maletín número {case_number} ya ha sido abierto o no existe.")

    def banker_offer(self):
        if len(self.remaining_cases) > 0:
            average_value = sum(self.remaining_cases.values()) / len(self.remaining_cases)
            offer = average_value * 0.75
            self.bank_offers.append(offer)
            return offer
        else:
            raise ValueError("No quedan maletines para hacer una oferta.")

    def final_choice(self, switch):
        """Final choice between keeping the selected case or switching with the last remaining case."""
        if switch:
            # Cambiar con el último maletín restante
            final_value = list(self.remaining_cases.values())[0]
        else:
            # Mantener el maletín seleccionado al inicio
            final_value = self.selected_case

        return final_value

    def reset_game(self):
        """Reinicia el juego para una nueva partida."""
        random.shuffle(self.cases)
        self.selected_case = None
        self.remaining_cases = {i: value for i, value in enumerate(self.cases, start=1)}
        self.opened_cases = []
        self.bank_offers = []
        self.current_round = 0
        self.cases_to_open = self.rounds[self.current_round]
