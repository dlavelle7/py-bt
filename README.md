# Behaviour Tree

[WIP]

Tree structure made up of Composite and Leaf nodes.

Leaf nodes are where the behaviour happens, for example an "action" or "test".

Composite nodes can be of 2 types:
* Sequence
* Selector

Sequence nodes return the first failed child node. Similar to the ALL operator.

Selector nodes return the first successful child node. Similar to the OR operator.

## Usage

Install:

```
python setup.py install
```

Define your desired tree model in JSON or YAML format (see Example section below for examples).

Define a python module for you behaviour tasks (actions & tests) and reference this in your tree model.

Then initialise and execute a behaviour tree object with some input data:

[TODO: Import path my change when proper setup.py written]

```
from bt.behaviour_tree import BehaviourTree

tree = BehaviourTree("/path/to/tree/model.json")
tree.load()

tree.execute(data)
```

## Example Models

Some example models can be found under the `/models` directory.

For example `/models/football/attacker.json` contains a behaviour tree for how a attacking player in a
football simulator might behave.


## Tests

```
pip install -r requirements.txt
pytest tests/
```

[TODO: CI Build]
[TODO: Docker build]
[TODO: Upload to pypi]
