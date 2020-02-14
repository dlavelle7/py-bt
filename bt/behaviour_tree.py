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
        self._execute(self.tree.get("children", []), data)

    def _execute(self, nodes, data):
        for node in nodes:
            if node.get("children") is not None:
                # TODO: handle, selector/sequence flow
                result = self._execute(node.get("children"), data)
            else:
                task = node.get("task")
                result = getattr(self.tasks_module, task)(data)
                if result is True:
                    self.executed_leaf = task  # TODO: could this be returned to execute()???
