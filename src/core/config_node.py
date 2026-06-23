
# -----------------------------------------------------------------------------
# src/core/config_node.py
# -----------------------------------------------------------------------------

from abc                    import ABC
from copy                   import deepcopy
from typing                 import Self

# -----------------------------------------------------------------------------
# Config
#
# * Gives access to BaseNode like config variable
# -----------------------------------------------------------------------------


class Config(ABC):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, config):
        self.config = BaseNode.create(config)

    def update(self, value: BaseNode) -> Self:
        self.config.update(value)
        return self

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# BaseNode
#
# * Base class and factory for all configuration nodes
# * Every node knows:
#   - its parent
#   - its Python name
#   - its JSON name
# -----------------------------------------------------------------------------


class BaseNode:
    # -------------------------------------------------------------------------
    # Utilities
    # -------------------------------------------------------------------------

    @staticmethod
    def python_to_json(name: str) -> str:
        return name.replace("_", "-")

    @staticmethod
    def json_to_python(name: str) -> str:
        return name.replace("-", "_")

    # -------------------------------------------------------------------------
    # Factory
    # -------------------------------------------------------------------------

    @classmethod
    def create(cls, value=None):
        return cls(value)

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, value = None, *, name=""):
        self._value = value
        self._name = name

    # -------------------------------------------------------------------------
    # Interfaces
    # -------------------------------------------------------------------------

    def is_dict(self):
        return isinstance(self._value, dict)

    def is_list(self):
        return isinstance(self._value, list)

    def is_primitive(self):
        return not isinstance(self._value, (dict, list))

    def get(self, default=None):
        if self.exists():
            return self._value

        return default

    def set(self, value):
        self._value = value

        return self

    def exists(self):
        return self._value is not None

    def clone(self):
        return BaseNode(
            deepcopy(self._value)
        )

    def update(self, other):
        if isinstance(other, BaseNode):
            other = other.get()

        if isinstance(self._value, dict) and isinstance(other, dict):
            self._value.update(other)
        else:
            self._value = other

        return self

    # -------------------------------------------------------------------------
    # Property
    # -------------------------------------------------------------------------

    @property
    def json_name(self):
        return BaseNode.python_to_json(self._name)

    # -------------------------------------------------------------------------
    # exists
    # -------------------------------------------------------------------------

    def __bool__(self):
        return bool(self._value)

    def __eq__(self, other):
        if isinstance(other, BaseNode):
            return self._value == other._value

        return self._value == other

    def equal(self, other):
        return (
            isinstance(other, BaseNode)
            and self.name == other.name
            and self._value == other._value
        )

    # -------------------------------------------------------------------------
    # Attribute access
    # -------------------------------------------------------------------------

    def __getattr__(self, name):
        return self._node(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        self._node(name, create=True).set(value)

    # -------------------------------------------------------------------------
    # List access
    # -------------------------------------------------------------------------

    def __getitem__(self, key):
        return self._node(key)

    def __setitem__(self, key, value):
        self._node(key, create=True).set(value)

    # -------------------------------------------------------------------------
    # Iteration
    # -------------------------------------------------------------------------

    def __iter__(self):
        if isinstance(self._value, dict):
            for key in self._value:
                yield self._node(JsonNaming.to_python(key))

        elif isinstance(self._value, list):
            for index in range(len(self._value)):
                yield self._node(index)

        else:
            return iter(())

    # -------------------------------------------------------------------------
    # Length
    # -------------------------------------------------------------------------

    def __len__(self):
        if isinstance(self._value, (dict, list)):
            return len(self._value)

        return 0

    # -------------------------------------------------------------------------
    # node handling
    # -------------------------------------------------------------------------

    def _dict_node(self, key, create=False):
        json_key = BaseNode.python_to_json(key)

        if json_key in self._value:
            return self._make_node(
                self._value[json_key],
                name=key
            )

        if create:
            self._value[json_key] = {}
            return self._make_node(
                self._value[json_key],
                name=key
            )

        return self._make_node(
            None,
            name=key
        )

    def _list_node(self, index, create=False):
        if not isinstance(index, int):
            return self._make_node(
                None,
                name=str(index)
            )

        if index < len(self._value):
            return self._make_node(
                self._value[index],
                name=f"[{index}]",
            )

        if create:
            while len(self._value) <= index:
                self._value.append(None)

            return self._make_node(
                self._value[index],
                name=f"[{index}]",
            )

        return self._make_node(
            None,
            name=f"[{index}]"
        )

    def _primitive_node(self, key, create=False):
        return self._make_node(
            None,
            name=str(key)
        )

    def _make_node(self, value, *, name=""):
        return BaseNode(
            value,
            name=name
        )

    def _node(self, key, create=False):
        if self.is_dict():
            return self._dict_node(key, create)

        if self.is_list():
            return self._list_node(key, create)

        return self._primitive_node(key, create)

    # -------------------------------------------------------------------------
    # strings
    # -------------------------------------------------------------------------
    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return (
            f"BaseNode("
            f"name='{self._name!r}', "
            f"exists={self.exists()}, "
            f"value={self._value!r})"
        )

# -----------------------------------------------------------------------------
