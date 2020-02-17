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
                "coordinates": (0, 1)
            },
            "opposition": [
                {
                    "name": "Jones",
                    "coordinates": (0, 2)
                }
            ],
            "teammates": []
        }
        self.btree.execute(game_data)
        self.assertListEqual(
            self.btree.execution_path,
            [
                ("check_have_space", True),
                ("check_close_to_goal", True),
                ("shoot", True)
            ]
        )

    def test_attacker_cannot_shoot_but_can_pass(self):
        game_data = {
            "attacker": {
                "name": "Mane",
                "coordinates": (1, 0)  # too far out to shoot
            },
            "opposition": [
                {
                    "name": "Jones",
                    "coordinates": (0, 1)
                }
            ],
            "teammates": [
                {
                    "name": "Robertson",
                    "coordinates": (1, 0)
                }
            ]
        }
        self.btree.execute(game_data)
        self.assertListEqual(
            self.btree.execution_path,
            [
                ("check_have_space", True),
                ("check_close_to_goal", False),
                ("check_have_space", True),
                ("check_teammate_nearby", True),
                ("pass_ball", True)]
        )

    # TODO
    def todo_test_attacker_cannot_shoot_can_could_cross(self):
        game_data = {
            "attacker": {
                "name": "Mane",
                "coordinates": (2, 0)  # too far out to shoot
            },
            "opposition": [
                {
                    "name": "Jones",
                    "coordinates": (0, 2)
                }
            ],
            "teammates": [
                {
                    "name": "Firmino",
                    "coordinates": (2, 0)
                }
            ]
        }
        self.btree.execute(game_data)
