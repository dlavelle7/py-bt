

def has_space(data):
    """Assume a defender is near if the nearest opposition player is less than 1m away."""
    nearest_opponent = data["opposition"][0]
    if nearest_opponent["proximity"] < 1:
        print(f"{nearest_opponent['name']} is closing down {data['attacker']['name']}.")
        return True
    print(f"No defender near {data['attacker']['name']} . . .")
    return False


def close_to_goal(data):
    """Attacker is close enough to goal for a shot if they are within 12m"""
    if data["attacker"]["distance_from_goal"] <= 12:
        print(f"{data['attacker']['name']} is close enough to shoot . . .") 
        return True
    print(f"{data['attacker']['name']} is not close enough to shoot . . .") 
    return False


def teammate_available(data):
    """An available teammate is withing 5m away."""
    for teammate in data["teammates"]:
        if teammate["proximity"] <= 5:
            print(f"{teammate['name']} is available . . .")
            return True
    print("No pass on")
    return False


def pass_ball(data):
    print(f"{data['attacker']['name']} passes the ball!")
    return True


def shoot(data):
    print(f"{data['attacker']['name']} shoots!")
    return True


def cross(data):
    print(f"{data['attacker']['name']} crosses the ball")
    return True
