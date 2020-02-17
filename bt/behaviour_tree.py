import os
import json
import importlib

from yaml import load

SEQUENCE = "sequence"
SELECTOR = "selector"


class BehaviourTree:

    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.tasks_path = None
        self.tasks_module = None
        self.executed_leaf = None

    def load(self):
        if self.file_path.endswith(".json"):
            self._load_json()
        elif self.file_path.endswith(".yaml"):
            self._load_yaml()
        else:
            raise TypeError(
                f"File type not supported for {os.path.basename(self.file_path)}. "
                "Please use JSON or YAML formats.")
        self.tasks_path = self.tree["path"]
        self.tasks_module = importlib.import_module(self.tasks_path)


    def _load_json(self):
        with open(self.file_path, "r") as json_file:
            self.tree = json.loads(json_file.read())

    def _load_yaml(self):
        with open(self.file_path, "r") as yaml_file:
            self.tree = load(yaml_file.read())

    def execute(self, data):
        print("Executing new flow")
        self._execute_node(self.tree, data)

    def _execute_node(self, node, data):
        for child in node.get("children"):
            if child.get("children") is not None:
                # TODO: handle, selector/sequence flow
                result = self._execute_node(child, data)
            else:
                task = child.get("task")
                result = getattr(self.tasks_module, task)(data)

            if node.get("type") == SEQUENCE:
                if result is False:
                    print(f"Sequence node {node} failed, returning")
                    return False
            elif node.get("type") == SELECTOR:
                if result is True:
                    print(f"Selector node {node} success, returning")
                    return True

        # TODO: if you added another node after pass (e.g. cross), it'd currently execute
        return result
