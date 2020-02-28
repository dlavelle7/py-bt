import os

from unittest import TestCase

from bt.behaviour_tree import BehaviourTree

YAML_MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "models/game/hungry_character.yaml"
    )
)


class TestFootball(TestCase):

    def setUp(self):
        self.btree = BehaviourTree(YAML_MODEL_PATH)
        self.btree.load()

    def test_can_eat_no_retry_needed(self):
        character_data = {
            "coordinates": (2, 2),
            "food": ["apple", "orange"],
        }
        self.btree.execute(character_data)
        self.assertListEqual(
            self.btree.execution_path,
            [
                ("am_i_hungry", True),
                ("have_i_food", True),
                ("NOT", ("enemies_nearby", False), True),
                ("eat", True)
            ]
        )
