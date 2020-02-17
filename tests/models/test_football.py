import os

from unittest import TestCase

from bt.behaviour_tree import BehaviourTree

JSON_TREE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "models/football/attacker.json"
    )
)


class TestFootball(TestCase):

    def setUp(self):
        self.btree = BehaviourTree(JSON_TREE_PATH)
        self.btree.load()

    def test_attacker_can_shoot(self):
        game_data = {
            "attacker": {
                "name": "Mane",
                "distance_from_goal": 9
            },
            "opposition": [
                {
                    "name": "Jones",
                    "proximity": 2
                }
            ],
            "teammates": []
        }
        self.btree.execute(game_data)
        self.assertEqual(self.btree.executed_leaf, "shoot")

    def test_attacker_cannot_shoot_but_can_pass(self):
        game_data = {
            "attacker": {
                "name": "Mane",
                "distance_from_goal": 20  # too far out to shoot
            },
            "opposition": [
                {
                    "name": "Jones",
                    "proximity": 2
                }
            ],
            "teammates": [
                {
                    "name": "Firmino",
                    "proximity": 3
                }
            ]
        }
        self.btree.execute(game_data)
        self.assertEqual(self.btree.executed_leaf, "pass_ball")
