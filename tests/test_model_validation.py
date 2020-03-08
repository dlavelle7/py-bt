from unittest import TestCase
from unittest.mock import patch

from jsonschema.exceptions import ValidationError
from bt.behaviour_tree import BehaviourTree


@patch("bt.behaviour_tree.importlib.import_module")
class TestValidation(TestCase):

    @patch("bt.behaviour_tree.BehaviourTree._load_json")
    def test_root_no_tasks_path(self, mock_load_json, mock_import):
        invalid_data = {
            "tree": {"task": "foo"}
        }
        mock_load_json.return_value = invalid_data
        bt = BehaviourTree("foobar.json")
        with self.assertRaises(ValidationError) as exc_context:
            bt.load()
        self.assertEqual(exc_context.exception.message,
                         "'tasks_path' is a required property")
        self.assertFalse(mock_import.import_module.called)

    @patch("bt.behaviour_tree.BehaviourTree._load_json")
    def test_root_no_tree(self, mock_load_json, mock_import):
        invalid_data = {
            "tasks_path": "foo.bar"
        }
        mock_load_json.return_value = invalid_data
        bt = BehaviourTree("foobar.json")
        with self.assertRaises(ValidationError) as exc_context:
            bt.load()
        self.assertEqual(exc_context.exception.message,
                         "'tree' is a required property")
        self.assertFalse(mock_import.import_module.called)

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
