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

    def test_can_eat_after_retry(self):
        # TODO:
        pass
