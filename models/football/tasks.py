import random

# 4 x 4 grid
PITCH = [
    [("cross",), ("shoot",), ("shoot",), ("cross",)],
    [("cross",), ("shoot",), ("shoot",), ("cross",)],
    [(), (), (), ()],
    [(), (), (), ()],
]


# Tests
def check_have_space(data, _):
    """An attacker has space if there is no defender in the same grid square"""
    for opponent in data["opposition"]:
        if opponent["coordinates"] == data["attacker"]["coordinates"]:
            print(f"{opponent['name']} is closing down {data['attacker']['name']}.")
            return False
    print(f"No defender near {data['attacker']['name']} . . .")
    return True


def check_close_to_goal(data, _):
    x, y = data["attacker"]["coordinates"]
    if "shoot" in PITCH[x][y]:
        print(f"{data['attacker']['name']} is close enough to shoot . . .")
        return True
    print(f"{data['attacker']['name']} is not close enough to shoot . . .")
    return False


def check_teammate_nearby(data, blackboard):
    """A nearby teammate is in the same grid square as the attacker on the ball."""
    nearby_teammates = []
    for teammate in data["teammates"]:
        if teammate["coordinates"] == data["attacker"]["coordinates"]:
            nearby_teammates.append(teammate)

    if nearby_teammates:
        blackboard[check_teammate_nearby.__name__] = nearby_teammates
        print(f"Teammates nearby . . .")
        return True
    print("No pass on")
    return False


def check_teammate_not_marked(data, blackboard):
    """A teammate is considered marked if there is an opponent in the same grid square."""
    available_teammates = []
    for teammate in blackboard[check_teammate_nearby.__name__]:
        for opponent in data["opposition"]:
            if teammate["coordinates"] != opponent["coordinates"]:
                available_teammates.append(teammate["name"])

    if available_teammates:
        blackboard[check_teammate_not_marked.__name__] = available_teammates
        print("Teammate not marked")
        return True
    print("All teammates are currently marked . . .")
    return False


def check_in_crossing_position(data, _):
    """Crossing position are the wings in the opponents half"""
    x, y = data["attacker"]["coordinates"]
    if "cross" in PITCH[x][y]:
        print(f"{data['attacker']['name']} is in crossing position . . .")
        return True
    print(f"{data['attacker']['name']} is not in a crossing position . . .")
    return False


# Actions
def pass_ball(data, blackboard):
    receiver = random.choice(blackboard[check_teammate_not_marked.__name__])
    print(f"{data['attacker']['name']} passes the ball to {receiver}!")
    return True


def shoot(data, _):
    print(f"{data['attacker']['name']} shoots!")
    return True


def cross(data, _):
    print(f"{data['attacker']['name']} crosses the ball!")
    return True


def go_backwards(data, _):
    print(f"No attacking options on, {data['attacker']['name']} goes backwards!")
    return True
