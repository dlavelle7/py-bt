import random


class DB:
    def query(self, table, **kwargs):
        return []


db = DB()


def am_i_hungry(_, __):
    # TODO: time since last meal?
    print("Feeling hungry . . .")
    return True


def have_i_food(data, _):
    if data["food"]:
        print("I have some food . . .")
        return True
    print("I have no food . . .")
    return False


def enemies_nearby(data, _):
    enemies = db.query("enemy", location=data["coordinates"])
    print(f"{len(enemies)} enemies in my vicinity . . .")
    if enemies:
        return True
    return False


def eat(data, _):
    food_item = random.choice(data["food"])
    print(f"Eating {food_item} . . .")
    return True
