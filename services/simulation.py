import random


def get_team_strength(user_cards: list) -> dict:
    """Считает силу команды на основе состава."""
    if not user_cards:
        return {"attack": 50, "defense": 50, "goalie": 50, "overall": 50}

    forwards = [uc for uc in user_cards if uc["card"].position in ["ЦН", "ЛП", "ПП"]]
    defenders = [uc for uc in user_cards if uc["card"].position == "З"]
    goalies = [uc for uc in user_cards if uc["card"].position == "В"]

    attack = sum(c["card"].shot + c["card"].pass_ + c["card"].speed for c in forwards) / (3 * max(len(forwards), 1))
    defense = sum(c["card"].defense + c["card"].physical for c in defenders) / (2 * max(len(defenders), 1)) if defenders else 50
    goalie = goalies[0]["card"].goalie if goalies else 50

    overall = (attack * 0.4 + defense * 0.3 + goalie * 0.3)
    return {"attack": attack, "defense": defense, "goalie": goalie, "overall": overall}


def simulate_match(team_strength: dict, opp_strength: int) -> dict:
    """Симуляция матча."""
    my_attack = team_strength["attack"]
    my_defense = team_strength["defense"]
    my_goalie = team_strength["goalie"]

    # Ожидаемые голы
    xg_my = max(0, (my_attack / 100) * 3.5 - (opp_strength / 100) * 1.5)
    xg_opp = max(0, (opp_strength / 100) * 3.5 - (my_defense / 100) * 1.5)

    # Симуляция
    goals_my = 0
    goals_opp = 0
    for _ in range(60):
        if random.random() < xg_my / 60:
            goals_my += 1
        if random.random() < xg_opp / 60:
            goals_opp += 1

    # Овертайм
    is_ot = False
    if goals_my == goals_opp:
        is_ot = True
        if random.random() < 0.5:
            goals_my += 1
        else:
            goals_opp += 1

    result = "win" if goals_my > goals_opp else "loss"
    if is_ot:
        result = "ot_win" if goals_my > goals_opp else "ot_loss"

    return {
        "goals_my": goals_my,
        "goals_opp": goals_opp,
        "result": result,
        "is_ot": is_ot,
        "xg_my": round(xg_my, 2),
        "xg_opp": round(xg_opp, 2),
  }
