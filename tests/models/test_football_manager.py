import os

from unittest import TestCase

from bt.behaviour_tree import BehaviourTree

JSON_TREE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "models/football_manager/attacker.json"
    )
)


class TestFootballManager(TestCase):

    def setUp(self):
        self.btree = BehaviourTree(JSON_TREE_PATH)
        self.btree.load()

    def test_attacker(self):
        game_data = {
            "attacker": {
                "name": "Mane"
            },
            "opposition": [
                {
                    "name": "Jones",
                    "proximity": 2
                }
            ]
        }
        self.btree.execute(game_data)
