import os

from unittest import TestCase

from bt.behaviour_tree import BehaviourTree

TREE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "models/football_manager/attacker_vs_defender.yaml"
    )
)


class TestFootballManager(TestCase):

    def test_attacker_has_ball(self):
        btree = BehaviourTree(TREE_PATH)
        btree.load()
        print(btree.tree)
