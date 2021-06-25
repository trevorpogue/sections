from copy import copy
from types import FunctionType
from typing import Any
from typing import List
from typing import Tuple

from .types import AnyDict
from .types import SectionAttr
from .types import SectionAttrs
from .types import SectionKeys
from .types import SectionKeysOrObjects
from .types import SectionNone
from .types import SectionParent
from .types import SectionType


class Meta(type):
    """
    Parses args and kwds passed to a sections() call or :class:`Section
    <Section>` instantiation and returns a Section tree structure. Parses
    node names/keys, separate attrs intended for current node vs child nodes,
    constructs current node, then recursively repeats for all child nodes.
    """

    singular_keyname = 'name'
    plural_keyname = 'names'
    default_keyvalue = SectionNone

    ##########################################################################
    #                   Tree structure node construction                     #

    def __call__(
            self,
            *args: SectionKeysOrObjects,
            parent: SectionParent = None,
            **kwds: SectionAttr
    ) -> SectionType:
        """
        Construct a tree structure of Section nodes based on the args and kwds
        provided by user in a sections() call or a Section() instantiation.
        """
        node_attrs, children_attrs, keyname = self._parse_attrs(
            args, kwds, parent)
        node = self._construct_node(parent, node_attrs)
        _construct_children(node, args, children_attrs, keyname)
        return node

    def _parse_attrs(
            self,
            args: SectionKeysOrObjects,
            kwds: SectionAttr,
            parent: SectionParent
    ) -> Tuple[SectionAttrs, SectionAttrs, str]:
        """
        From user-provided args and kwds in a sections() or Section() call,
        parse node names/keys, separate attrs intended for current node vs
        child nodes, construct current node, then recursively repeat for all
        child nodes.
        """
        node_attrs, children_attrs = {}, {}
        keyname = self.singular_keyname
        keys = self._parse_keys(args, kwds, keyname)
        for k, v in {**kwds, **keys}.items():
            _parse_node_attrs(k, v, node_attrs, children_attrs)
        self._fix_key_if_invalid(node_attrs, parent, keyname)
        node_attrs['_keyname'] = keyname
        return node_attrs, children_attrs, keyname

    def _parse_keys(
            self,
            args: SectionKeysOrObjects,
            kwds: SectionAttr,
            keyname: str
    ) -> None:
        keys = {}
        if _dict_haskey(kwds, keyname):
            keys[keyname] = kwds.get(keyname)
        if (not _dict_haskey(kwds, keyname)
                and _dict_haskey(kwds, self.plural_keyname)):
            keys[keyname] = kwds.get(self.plural_keyname)
        if not _dict_haskey(keys, keyname):
            keys[keyname] = self._getkeys_from_argskwds(args, kwds)
        return keys

    def _getkeys_from_argskwds(
            self,
            args: SectionKeysOrObjects,
            kwds: SectionAttrs
    ) -> SectionKeys:
        """
        Parse keys from args or kwds if it wasn't explicitly provided in kwds.
        """
        if len(args) == 1 and not isinstance(args[0], list):
            # if given a single non-list argument it will be used only as
            # current node's name/key
            return list(args)[0]
        elif len(args) >= 1:
            # otherwise if any arguments were given, they are for at least
            # one child's' names/keys, and possibly the current node's also
            return list(args)
        else:
            # otherwise, use the default for the current node
            return self.default_keyvalue

    def _fix_key_if_invalid(
            self, attrs: SectionAttrs, parent: SectionParent, keyname: str
    ) -> None:
        """
        Enforce that node must have a keyname attr, and disallow key values
        from properties and FunctionTypes.
        """
        default_keyvalue = (self.default_keyvalue if parent is None
                            else parent.nofchildren)
        keyvalue = attrs.get(keyname, default_keyvalue)
        if (isinstance(keyvalue, FunctionType)
                or isinstance(keyvalue, property)):
            keyvalue = default_keyvalue
        attrs[keyname] = keyvalue

    def _construct_node(
            self, parent: SectionParent, attrs: SectionAttrs
    ) -> SectionType:
        """
        Construct current node by providing node all its attrs, then update
        tree structure's class with any provided propertied or methods.
        """
        class_attrs, node_attrs = {}, {}
        for k, v in attrs.items():
            if isinstance(v, FunctionType) or isinstance(v, property):
                class_attrs[k] = v
            else:
                node_attrs[k] = v
        node = super().__call__(parent=parent, **node_attrs)
        for k, v in class_attrs.items():
            setattr(node.__class__, k, v)
        return node


def _construct_children(
    node: SectionType,
    args: SectionKeysOrObjects,
    children_attrs: SectionAttrs,
    keyname: str
) -> None:
    """
    Recursively repeat construction per child with extracted child attrs.
    """
    nofchildren_from_attrs, children_from_args = (
        _get_children_data(node, args, children_attrs)
    )
    for child in children_from_args:
        node[getattr(child, keyname)] = child
    for child_i in range(nofchildren_from_attrs):
        _contruct_child(child_i, children_attrs, node, keyname)


def _get_children_data(
        node: SectionType,
        args: SectionKeysOrObjects,
        attrs: SectionAttrs
) -> Tuple[int, List[SectionType]]:
    """
    Return number of children nodes implied by provided self.__call__ kwds,
    and any pre-constructed Section children passed in self.__call__ args.
    """
    nofchildren_from_attrs = (
        max(_len(v) for v in attrs.values()) if attrs else 0)
    children_from_args = []
    for arg in args:
        from . import Section
        if isinstance(arg, Section):
            children_from_args += [arg]
    return (nofchildren_from_attrs, children_from_args)


def _contruct_child(
        child_i: int, children_attrs: SectionAttrs,
        node: SectionType, keyname: str
) -> None:
    """Parse attr[i] from each attr and give to child."""
    child_attrs = {}
    for k, v in children_attrs.items():
        if len(v) > child_i:
            child_attrs[k] = v[child_i]
    key = child_attrs.get(keyname, child_i)
    child_attrs[keyname] = key
    child = _get_dictval_i(node, child_i)
    if child is None:
        child = node.__class__(parent=node, **child_attrs)
    node[getattr(child, keyname)] = child


def _len(x: Any) -> int:
    """Return len of x if it is iterable, else 0."""
    return max(1, len(x)) if isinstance(x, list) else 0


def _dict_haskey(d: AnyDict, key: Any) -> bool:
    """
    Return True if dict contains user-provided value for key, else False.
    """
    return d.get(key, SectionNone) is not SectionNone


def _get_dictval_i(d: AnyDict, i: int) -> Any:
    """Get value in iterator position i from dict as if its a list."""
    ret = None
    for ii, value in enumerate(d.values()):
        if ii == i:
            ret = value
            break
    return ret


def _parse_node_attrs(
        name: str, value: Any, node_attrs: SectionAttrs,
        children_attrs: SectionAttrs
) -> None:
    """
    Extract attrs intended for current node from user-provided args/kwds.
    """
    if not isinstance(value, list):
        node_attrs[name] = value
    else:
        if len(value) > 0 and isinstance(value[0], set):
            value = copy(value)
            node_attrs[name] = value.pop(0).copy().pop()
        children_attrs[name] = value
