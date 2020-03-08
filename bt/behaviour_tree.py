import os
import json
import yaml
import importlib
import jsonschema

from bt.logger import logger

TREE = "tree"
SEQUENCE = "sequence"
SELECTOR = "selector"
TASK = "task"
DECORATOR_NOT = "not"
DECORATOR_RETRY = "retry"
RETRY_COUNT = "count"
DEFAULT_RETRY_COUNT = 1

# TODO: refactor json schema (reuse "nodes")
# TODO: XML support
# TODO: Parallel children? e.g. success if 3 / 5 children succeed
# TODO: Subtrees
# TODO: Restrict node blackboard access - within family?

MODEL_SCHEMA_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "model_schema.json"
    )
)


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
            self.model = self._load_json()
        elif self.file_path.endswith(".yaml") or self.file_path.endswith(".yml"):
            self.model = self._load_yaml()
        else:
            raise TypeError(
                f"File type not supported for {os.path.basename(self.file_path)}. "
                "Please use JSON or YAML formats.")
        self._validate_model()
        logger.info("Model validated successfully.")
        self.tasks_path = self.model["tasks_path"]
        self.tasks_module = importlib.import_module(self.tasks_path)

    def _load_json(self):
        with open(self.file_path, "r") as json_file:
            return json.loads(json_file.read())

    def _load_yaml(self):
        with open(self.file_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file.read())

    def _validate_model(self):
        with open(MODEL_SCHEMA_PATH, "r") as json_file:
            schema = json.loads(json_file.read())
        jsonschema.validate(instance=self.model, schema=schema)

    def execute(self, data):
        self.execution_path = []
        self.blackboard = {}
        logger.info("Executing behaviour tree")
        self._execute_node(self.model[TREE], data)
        logger.info("Finished executing behaviour tree")

    def _get_composite_node_type_and_children(self, node):
        if node.get(SEQUENCE) is not None:
            return SEQUENCE, node[SEQUENCE]
        elif node.get(SELECTOR) is not None:
            return SELECTOR, node[SELECTOR]
        elif node.get(DECORATOR_NOT) is not None:
            return DECORATOR_NOT, [node[DECORATOR_NOT]]
        elif node.get(DECORATOR_RETRY) is not None:
            return DECORATOR_RETRY, [node[DECORATOR_RETRY]]

    def _execute_node(self, node, data):
        if node.get(TASK) is not None:
            task = node[TASK]
            child_result = getattr(self.tasks_module, task)(data, self.blackboard)
            self.execution_path.append((task, child_result))
            return child_result
        else:
            node_type, children = self._get_composite_node_type_and_children(node)

        for child in children:
            child_result = self._execute_node(child, data)
            if node_type == DECORATOR_RETRY:
                retry_count = node[DECORATOR_RETRY].get(RETRY_COUNT, DEFAULT_RETRY_COUNT)
                while retry_count > 0 and child_result is False:
                    logger.info(f"Retrying decorator node: {retry_count} reties left.")
                    retry_count -= 1
                    child_result = self._execute_node(child, data)
            elif node_type == DECORATOR_NOT:
                self.execution_path[-1] = (DECORATOR_NOT.upper(), self.execution_path[-1], not child_result)
                child_result = not child_result
            elif node_type == SEQUENCE:
                if child_result is False:
                    logger.info(f"Sequence node child failed, returning")
                    return False
            elif node_type == SELECTOR:
                if child_result is True:
                    logger.info(f"Selector node child success, returning")
                    return True

        return child_result
