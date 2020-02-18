import os
import json
import importlib

from yaml import load

from bt.logger import logger

SEQUENCE = "sequence"
SELECTOR = "selector"

# TODO: Subtrees
# TODO: an inverter node would be more readable than "check_not_()" tasks
# TODO: Restrict node blackboard access - within family?


class BehaviourTree:

    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.tasks_path = None
        self.tasks_module = None
        self.execution_path = []
        self.blackboard = {}

    def load(self):
        if self.file_path.endswith(".json"):
            self._load_json()
        elif self.file_path.endswith(".yaml"):
            self._load_yaml()
        else:
            raise TypeError(
                f"File type not supported for {os.path.basename(self.file_path)}. "
                "Please use JSON or YAML formats.")
        self.tasks_path = self.tree["tasks_path"]
        self.blackboard[self.tasks_path] = {}
        self.tasks_module = importlib.import_module(self.tasks_path)

    def _load_json(self):
        with open(self.file_path, "r") as json_file:
            self.tree = json.loads(json_file.read())

    def _load_yaml(self):
        with open(self.file_path, "r") as yaml_file:
            self.tree = load(yaml_file.read())

    def execute(self, data):
        logger.info("\nExecuting new flow")
        self._execute_node(self.tree, data)

    def _execute_node(self, node, data):
        for child in node.get("children"):
            if child.get("children") is not None:
                child_result = self._execute_node(child, data)
            else:
                task = child.get("task")
                child_result = getattr(self.tasks_module, task)(data, self.blackboard[self.tasks_path])
                self.execution_path.append((task, child_result))

            if node.get("type") == SEQUENCE:
                if child_result is False:
                    logger.info(f"Sequence node child failed, returning")
                    return False
            elif node.get("type") == SELECTOR:
                if child_result is True:
                    logger.info(f"Selector node child success, returning")
                    return True

        return child_result
