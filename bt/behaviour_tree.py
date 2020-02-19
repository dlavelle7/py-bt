import os
import json
import importlib

from yaml import load

from bt.logger import logger

TREE = "tree"
SEQUENCE = "sequence"
SELECTOR = "selector"
TASK = "task"

# TODO: Subtrees
# TODO: Validate tree in load() -> Use JSON Schema/Marshmallow -> Composites can only be sel/seq, Leafs can only be task
# TODO: Decorators: Retry, Inverter would be more readable than "check_not_()" tasks
# TODO: Restrict node blackboard access - within family?


class BehaviourTree:

    def __init__(self, file_path):
        self.file_path = file_path
        self.model = None
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
        self.tasks_path = self.model["tasks_path"]
        self.tasks_module = importlib.import_module(self.tasks_path)

    def _load_json(self):
        with open(self.file_path, "r") as json_file:
            self.model = json.loads(json_file.read())

    def _load_yaml(self):
        with open(self.file_path, "r") as yaml_file:
            self.model = load(yaml_file.read())

    def execute(self, data):
        self.blackboard = {}
        logger.info("\nExecuting new flow")
        self._execute_node(self.model[TREE], data)

    def _execute_node(self, node, data):
        if node.get(SEQUENCE) is not None:
            node_type = SEQUENCE
            children = node[SEQUENCE]
        elif node.get(SELECTOR) is not None:
            node_type = SELECTOR
            children = node[SELECTOR]
        else:
            task = node[TASK]
            child_result = getattr(self.tasks_module, task)(data, self.blackboard)
            self.execution_path.append((task, child_result))
            return child_result

        for child in children:
            child_result = self._execute_node(child, data)

            if node_type == SEQUENCE:
                if child_result is False:
                    logger.info(f"Sequence node child failed, returning")
                    return False
            elif node_type == SELECTOR:
                if child_result is True:
                    logger.info(f"Selector node child success, returning")
                    return True

        return child_result
