"""
Flexible tree data structures for organizing lists and dicts into sections.

https://github.com/trevorpogue/sections
"""

from typing import Any
from typing import List
from typing import Type
from typing import Union

from .attr_parser import AttrParser
from .dict import Dict
from .meta import Meta
from .node import Node
from .string_parser import StringParser
from .types import GetType
from .types import SectionAttrs
from .types import SectionType


class Section(Node, Dict, AttrParser, StringParser, dict,
              metaclass=Meta):
    """
    Objects instantiated by :class:`Section <Section>` are nodes in a sections
    tree structure. Each node has useful methods and properties for organizing
    lists/dicts into sections and for conveniently accessing/modifying the
    sub-list/dicts from each section/subsection.
    """

    ##########################################################################
    #              tree-structure-wide attributes for every node             #

    # class attributes act as tree-structure-wide attributes across all nodes.
    # This is possible because each sections() module call returns a unique
    # copy of the Section class, giving each individual structure its own class

    # Choose whether to use a cache in each node. The cache contains
    # quickly-readable references to attribute iterables parsed from manually
    # traversing through descendant nodes in a previous read. The caches are
    # invalidated when the tree structure or node attribute values change.
    # Using the cache can often make structure attribute reading faster by 5x
    # and even much more. The downside is that it also increases memory used by
    # roughly 5x as well. This is not a concern on a general-purpose computer
    # for structures containing less than 1000 nodes or 10,000 nodes, although
    # further testing is required to confirm this. After 10,000 nodes, it may
    # be recommended to turn the structure class attribute `use_cache` to
    # False.
    use_cache = True

    # See method Section.get_nearest_attr's doctring for a full description of
    # gettype and its default value. 'hybrid' returns a list if more than 1
    # element is found, else return the non-iterable raw form of the element
    default_gettype = 'hybrid'

    use_pluralsingular = True
    ##########################################################################

    def __init__(self, **kwds: SectionAttrs) -> None:
        """Set object attr for every attr in kwds and init attr cache."""
        if self.use_cache and self.isleaf:
            self._cache = {}
        for name, value in kwds.items():
            self.__setattr__(name, value, _invalidate_cache=False)

    @property
    def cls(self) -> Type[SectionType]:
        """The unique structure-wide class of each node."""
        return self.__class__

    @ property
    def sections(self) -> SectionType:
        """A synonym for property :meth:`children <Section.children>`."""
        return self.children

    @ property
    def entries(self) -> SectionType:
        """A synonym for property :meth:`leaves <Section.leaves>`."""
        return self.leaves

    def __call__(
            self,
            name: str,
            gettype: GetType = 'default'
    ) -> Union[Any, List[Any]]:
        """
        Run :meth:`get_nearest_attr <Section.get_nearest_attr>`. This
        returns attribute `name` from self if self contains the attribute in
        either the singular or plural form for `name`. Else, try the same
        pattern for each of self's children, putting the returned results from
        each child into a list. Else, raise AttributeError.

        For argument `gettype`, Setting to `'default'` uses the value of
        self.default_gettype for gettype (its default is 'hybrid'). Setting to
        `'hybrid'` returns a list if more than 1 element is found, else returns
        the non-iterable raw form of the element. Setting to `list` returns a
        list containing the attribute values. Setting to `iter` returns an
        iterable iterating through the attribute values. Setting to `dict`
        returns a dict containing pairs of the containing node's name with the
        attribute value. Setting to `'full_dict'` is faster than `dict` and
        returns a dict containing pairs of a reference to each node and its
        attribute value. `'full_dict'` output is visually identical to `dict`
        for printing purposes except that it will contain all attributes even
        if some source nodes have duplicate names. The only downside to
        `'full_dict'` is that the keys cannot be referenced by name like with
        `dict`, but all values() are still valid.

        :param name: The name of the attribute to find in self or self's
                     descendants.

        :param gettype: Valid values are `'default'`, `'hybrid'` `list`,
                        `iter`, `dict`, `'full_dict'`. See method's description
                        body above for explanation of what each value does.

        :return: An iterable or non-iterable form of the attribute `name`
                 formed from self or descendant nodes. Depends on the value
                 given to `gettype`.
        """
        return self.get_nearest_attr(name, gettype=gettype)
