
def am_i_hungry(_, __):
    # TODO: time since last meal?
    print("Feeling hungry . . .")
    return True


def have_i_food(data, _):
    # TODO: check if someting in data['food']
    print("I have some food . . .")
    return True


def enemies_nearby(data, _):
    # TODO: Maybe this would be a request to an external api, as the environment changes
    pass


def eat(data, _):
    # TODO: Randmoly eat an item in data['food']
    print(f"Eating an . . .")
