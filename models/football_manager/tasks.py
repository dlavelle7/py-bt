

def dribble(data):
    print(f"Attacker {data['attacker']['name']} is dribbling . . .")


def is_defender_near(data):
    """Assume a defender is near if the nearest opposition player is less than 1m away."""
    nearest_opponent = data["opposition"][0]
    if nearest_opponent["proximity"] < 1:
        print(f"{nearest_opponent['name']} is closing down {data['attacker']['name']}.")
    print(f"No defender near {data['attacker']['name']} . . .")
    return False


def cross(data):
    # TODO: pass data
    print("{data['attacker']['name']} crosses the ball")
