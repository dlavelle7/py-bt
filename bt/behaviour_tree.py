from yaml import load


class BehaviourTree:

    def __init__(self, tree_path):
        self.tree_path = tree_path
        self.tree = None

    def load(self):
        with open(self.tree_path, "r") as yaml_file:
            self.tree = load(yaml_file.read())
