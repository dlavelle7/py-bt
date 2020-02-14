import os
import json
import importlib

from yaml import load


class BehaviourTree:

    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.tasks_path = None
        self.tasks_module = None

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
        self._execute(self.tree.get("children", []), data)

    def _execute(self, nodes, data):
        # TODO: handle, selector/sequence flow
        for node in nodes:
            if node["type"] in ("sequence", "selector"):
                result = self._execute(node, data)
            elif node["type"] == "leaf":
                if node.get("action") is not None:
                    action = node.get("action")
                    try:
                        result = getattr(self.tasks_module, action)(data)
                    except ActionError as exc:
                        print(f"Exception {exc}.")
                        # TODO: handle action failure
                elif node.get("test") is not None:
                    condition = node.get("test")
                    test_passed = getattr(self.tasks_module, condition)(data)
                    # TODO: handle test failure
