# 4 x 4 grid
PITCH = [
    [("cross",), ("shoot",), ("shoot",), ("cross",)],
    [("cross",), ("shoot",), ("shoot",), ("cross",)],
    [(), (), (), ()],
    [(), (), (), ()],
]

# Tests
def check_have_space(data):
    """An attacker has space if there is no defender in the same grid square"""
    for opponent in data["opposition"]:
        if opponent["coordinates"] == data["attacker"]["coordinates"]:
            print(f"{opponent['name']} is closing down {data['attacker']['name']}.")
            return False
    print(f"No defender near {data['attacker']['name']} . . .")
    return True


def check_close_to_goal(data):
    x, y = data["attacker"]["coordinates"]
    if "shoot" in PITCH[x][y]:
        print(f"{data['attacker']['name']} is close enough to shoot . . .") 
        return True
    print(f"{data['attacker']['name']} is not close enough to shoot . . .") 
    return False


def check_teammate_nearby(data):
    """A nearby teammate is in the same grid square as the attacker on the ball."""
    for teammate in data["teammates"]:
        if teammate["coordinates"] == data["attacker"]["coordinates"]:
            print(f"{teammate['name']} is nearby . . .")
            return True
    print("No pass on")
    return False


def check_in_crossing_position(data):
    """Crossing position are the wings in the opponents half"""
    x, y = data["attacker"]["coordinates"]
    if "cross" in PITCH[x][y]:
        print(f"{data['attacker']['name']} is in crossing position . . .") 
        return True
    print(f"{data['attacker']['name']} is not in a crossing position . . .") 
    return False


# Actions
def pass_ball(data):
    print(f"{data['attacker']['name']} passes the ball!")
    return True


def shoot(data):
    print(f"{data['attacker']['name']} shoots!")
    return True


def cross(data):
    print(f"{data['attacker']['name']} crosses the ball")
    return True
