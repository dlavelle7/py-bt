import os

from unittest import TestCase
from unittest.mock import patch

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

    @patch("models.game.tasks.DB.query", side_effect=[["Bowser", "Revolver Ocelot"], ["Ricardo Diaz", "Marlene"]])
    def test_can_eat_after_2_retries(self, mock_db_query):
        """Mock the db call to check for enemies around to pass on the 3rd attempt."""
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
                ("NOT", ("enemies_nearby", True), False),
                ("RETRY", ("NOT", ("enemies_nearby", True), False), False),
                ("RETRY", ("NOT", ("enemies_nearby", False), True), True),
                ("eat", True)
            ]
        )
