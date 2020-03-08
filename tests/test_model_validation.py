from unittest import TestCase
from unittest.mock import patch

from jsonschema.exceptions import ValidationError
from bt.behaviour_tree import BehaviourTree


@patch("bt.behaviour_tree.importlib.import_module")
class TestValidation(TestCase):

    # TODO: test 2 root fields
    # safe yaml load

    @patch("bt.behaviour_tree.BehaviourTree._load_json")
    def test_decorator_with_invalid_child_node_key(self, mock_load_json, mock_import):
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
        with self.assertRaises(ValidationError) as exc_context:
            bt.load()
        self.assertEqual(exc_context.exception.message,
                         "Additional properties are not allowed ('BAD_KEY' was unexpected)")
        self.assertFalse(mock_import.import_module.called)

    @patch("bt.behaviour_tree.BehaviourTree._load_yaml")
    def test_composite_with_invalid_child_node_value(self, mock_load_yaml, mock_import):
        invalid_data = {
            "tasks_path": "foo.bar",
            "tree": {
                "sequence": [
                    {
                        "retry": {
                            "selector": [
                                {
                                    "task": "good_value",
                                },
                                {
                                    "task": {"BAD_KEY": "BAD_VALUE"}
                                }
                            ]
                        }
                    },
                    {
                        "task": "another_good_value"
                    }
                ]
            }
        }
        mock_load_yaml.return_value = invalid_data
        bt = BehaviourTree("foobar.yaml")
        with self.assertRaises(ValidationError) as exc_context:
            bt.load()
        self.assertEqual(exc_context.exception.message,
                         "{'BAD_KEY': 'BAD_VALUE'} is not of type 'string'")
        self.assertFalse(mock_import.import_module.called)
