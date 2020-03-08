from unittest import TestCase
from unittest.mock import patch

from jsonschema.exceptions import ValidationError
from bt.behaviour_tree import BehaviourTree


@patch("bt.behaviour_tree.importlib.import_module")
class TestValidation(TestCase):

    @patch("bt.behaviour_tree.BehaviourTree._load_json")
    def test_decorator_recursive_error(self, mock_load_json, mock_import):
        invalid_data = {
            "tasks_path": "foo.bar",
            "tree": {
                "selector": [
                    {"task": "foo"},
                    {"not": {"BAD_KEY": "bar"}}
                ]
            }
        }
        mock_load_json.return_value = invalid_data
        bt = BehaviourTree("foobar.json")
        self.assertRaises(ValidationError, bt.load)
