from flask import Blueprint, render_template, request, redirect, url_for
from game.game_logic import DealOrNoDeal

game_bp = Blueprint('juegos', __name__, template_folder="templates/game", static_folder="static")
game = DealOrNoDeal()

@game_bp.route('/games')
def index():
    return render_template('game.html')

@game_bp.route('/select_case', methods=['POST'])
def select_case():
    case_number = int(request.form['case_number'])
    game.select_case(case_number)
    return redirect(url_for('juegos.open_case_screen'))

@game_bp.route('/open_case_screen')
def open_case_screen():
    opened_case_numbers = [case[0] for case in game.opened_cases]
    selected_case_number = None
    if game.selected_case is not None:
        for k, v in game.remaining_cases.items():
            if v == game.selected_case:
                selected_case_number = k
                break
    
    return render_template(
        'open_case.html',
        remaining_cases=len(game.remaining_cases),
        opened_case_numbers=opened_case_numbers,
        selected_case_number=selected_case_number
    )

@game_bp.route('/open_case', methods=['POST'])
def open_case():
    case_number = int(request.form['case_number'])
    try:
        case_value = game.open_case(case_number)
        remaining_cases = len(game.remaining_cases)

        if remaining_cases in [20, 15, 11, 8, 6, 5, 4, 3, 2, 1]:
            offer = game.banker_offer()
            return render_template('deal_no_deal.html', case_value=case_value, offer=offer)

        return render_template('open_case.html', case_value=case_value, remaining_cases=remaining_cases)
    except ValueError as e:
        return str(e), 400

@game_bp.route('/deal_no_deal', methods=['POST'])
def deal_no_deal():
    deal = request.form['deal'].strip().lower()
    opened_case_numbers = [case[0] for case in game.opened_cases]
    selected_case_number = None
    if game.selected_case is not None:
        for k, v in game.remaining_cases.items():
            if v == game.selected_case:
                selected_case_number = k
                break
    
    if deal == 'deal':
        offer = game.bank_offers[-1]
        return render_template('final.html', message=f"¡Te llevas la oferta del banquero de ${offer:.2f}!")
    else:
        return render_template(
            'deal_no_deal.html', 
            deal=deal, 
            opened_case_numbers=opened_case_numbers, 
            selected_case_number=selected_case_number
        )

@game_bp.route('/final_round', methods=['POST'])
def final_round():
    final_decision = request.form['final_decision'].strip().lower()
    if final_decision == 'cambiar':
        final_value = game.final_choice(switch=True)  # Cambiar al último maletín restante
    else:
        final_value = game.final_choice(switch=False)  # Mantener el maletín seleccionado

    return render_template('final.html', message=f"¡Tu maletín contiene ${final_value:.2f}!")

@game_bp.route('/game_history')
def game_history():
    return render_template('game_history.html', results=game.bank_offers)

@game_bp.route('/revealed_cases')
def revealed_cases():
    # Retrieve the cases that have been revealed (excluding the initial selected case)
    revealed_cases = [(case[0], case[1]) for case in game.opened_cases]
    
    return render_template('revealed_cases.html', revealed_cases=revealed_cases)
from flask import Blueprint, render_template, request, redirect, url_for
from game.game_logic import DealOrNoDeal

game_bp = Blueprint('juegos', __name__, template_folder="templates/game", static_folder="static")
game = DealOrNoDeal()

@game_bp.route('/games')
def index():
    return render_template('game.html')

@game_bp.route('/select_case', methods=['POST'])
def select_case():
    case_number = int(request.form['case_number'])
    game.select_case(case_number)
    return redirect(url_for('juegos.open_case_screen'))


@game_bp.route('/select_main_case', methods=['POST'])
def select_main_case():
    case_number = int(request.form['case_number'])
    try:
        game.select_main_case(case_number)
        return redirect(url_for('juegos.open_case_screen'))
    except ValueError as e:
        return str(e), 400

@game_bp.route('/open_case_screen')
def open_case_screen():
    opened_case_numbers = [case[0] for case in game.opened_cases]
    selected_case_number = None
    if game.selected_case is not None:
        for k, v in game.remaining_cases.items():
            if v == game.selected_case:
                selected_case_number = k
                break
    
    return render_template(
        'open_case.html',
        remaining_cases=len(game.remaining_cases),
        opened_case_numbers=opened_case_numbers,
        selected_case_number=selected_case_number
    )

@game_bp.route('/open_case', methods=['POST'])
def open_case():
    case_number = int(request.form['case_number'])
    try:
        case_value = game.open_case(case_number)
        remaining_cases = len(game.remaining_cases)

        if remaining_cases in [20, 15, 11, 8, 6, 5, 4, 3, 2, 1]:
            offer = game.banker_offer()
            return render_template('deal_no_deal.html', case_value=case_value, offer=offer)

        return render_template('open_case.html', case_value=case_value, remaining_cases=remaining_cases)
    except ValueError as e:
        return str(e), 400

@game_bp.route('/deal_no_deal', methods=['POST'])
def deal_no_deal():
    deal = request.form['deal'].strip().lower()
    opened_case_numbers = [case[0] for case in game.opened_cases]
    selected_case_number = None
    if game.selected_case is not None:
        for k, v in game.remaining_cases.items():
            if v == game.selected_case:
                selected_case_number = k
                break
    
    if deal == 'deal':
        offer = game.bank_offers[-1]
        return render_template('final.html', message=f"¡Te llevas la oferta del banquero de ${offer:.2f}!")
    else:
        return render_template(
            'deal_no_deal.html', 
            deal=deal, 
            opened_case_numbers=opened_case_numbers, 
            selected_case_number=selected_case_number
        )

@game_bp.route('/final_round', methods=['POST'])
def final_round():
    final_decision = request.form['final_decision'].strip().lower()
    if final_decision == 'cambiar':
        final_value = game.final_choice(switch=True)  # Cambiar al último maletín restante
    else:
        final_value = game.final_choice(switch=False)  # Mantener el maletín seleccionado

    return render_template('final.html', message=f"¡Tu maletín contiene ${final_value:.2f}!")

@game_bp.route('/game_history')
def game_history():
    return render_template('game_history.html', results=game.bank_offers)

@game_bp.route('/revealed_cases')
def revealed_cases():
    # Retrieve the cases that have been revealed (excluding the initial selected case)
    revealed_cases = [(case[0], case[1]) for case in game.opened_cases]
    
    return render_template('revealed_cases.html', revealed_cases=revealed_cases)