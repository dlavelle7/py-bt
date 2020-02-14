# Behaviour Tree

Tree structure made up of Composite and Leaf nodes.

Leaf nodes are where the behaviour happens, for example an "action" or "test".

Composite nodes can be of 2 types:
* Sequence
* Selector

Sequence nodes return the first failed child node. Similar to the ALL operator.

Selector nodes return the first successful child node. Similar to the OR operator.

[TODO] Football Manager Sim: Attacker behaviour
* Dribble forward
* Defender in vicinity?
* Cross ball
