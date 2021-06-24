"""
Flexible tree data structures for organizing lists and dicts into sections.
https://github.com/trevorpogue/sections
"""

from copy import copy
from itertools import chain
from itertools import repeat
from types import FunctionType
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import NewType
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

from pluralizer import Pluralizer

# SectionAttrs: dict containing user-defined attributes to set for Section
# object nodes. It may also contain a few internally-provided attributes such
# as `parent`, and `name`.
SectionAttr = NewType('SectionAttr', Any)
SectionAttrs = NewType('SectionAttrs', Dict[Any, SectionAttr])

# Represents sections.Section type since cannot define sections.Section yet
Section = NewType('Section', object)

# SectionKeysOrObjects: A List that contains either a Section key, a Section
# object, a set of one of those, or an arbitrarily deep nested list of the
# previously mentioned items
SectionKeysOrObjects = NewType(
    'SectionKeysOrObjects', List[Union[Any, Set[Any], Section, List[Any]]]
)

# Contains either a Section key, or an arbitrarily deep nested list of them
SectionKeys = NewType('SectionKeys', Union[Any, List[Any]])

# parent can be either another Section object or None (if node is root)
SectionParent = NewType('SectionParent', Union[Section, None])

# A shorthand form for an arbitrary dict
AnyDict = NewType('AnyDict', Dict[Any, Any])

# Valid values for the class Section.gettype:
default = NewType('default', 'default')       # use self.default_gettype
# use hybrid getattr method (see Section.__call__ docstring for more info
hybrid = NewType('hybrid', 'hybrid')
# use full_dict getattr method (see Section.__call__ docstring for more info)
full_dict = NewType('full_dict', 'full_dict')
GetType = NewType('GetType', Union[
    default, hybrid, list, iter, dict, full_dict
])


class SectionNoneType:
    """
    Indicates the absence of a value as opposed to any possible user-defined
    value that can be given to an attribute. Using this instead of None allows
    users to still set attribute values to None without unexpected behaviour.
    The __str__ override returns `"section"` because a SectionNoneType object
    is used for the keys/names of unnamed nodes, and printing 'section' as the
    node's name makes its printed representation look more sensical.
    """

    def __str__(self) -> str: return 'section'


class MetaSection(type):
    """
    Parses args and kwds passed to a sections() call or :class:`Section
    <Section>` instantiation and returns a Section tree structure. Parses
    node names/keys, separate attrs intended for current node vs child nodes,
    constructs current node, then recursively repeats for all child nodes.
    """
    _None = SectionNoneType()
    singular_keyname = 'name'
    plural_keyname = 'names'
    default_keyvalue = _None

    ##########################################################################
    #                   Tree structure node construction                     #

    def __call__(
            self,
            *args: SectionKeysOrObjects,
            parent: SectionParent = None,
            **kwds: SectionAttr
    ) -> Section:
        """
        Construct a tree structure of Section nodes based on the args and kwds
        provided by user in a sections() call or a Section() instantiation.
        """
        node_attrs, children_attrs, keyname = self._parse_attrs(
            args, kwds, parent)
        node = self._construct_node(parent, node_attrs)
        self._construct_children(node, args, children_attrs, keyname)
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
        keys = {}
        if self._dict_haskey(kwds, keyname):
            keys[keyname] = kwds.get(keyname)
        if (not self._dict_haskey(kwds, keyname)
                and self._dict_haskey(kwds, self.plural_keyname)):
            keys[keyname] = kwds.get(self.plural_keyname)
        if not self._dict_haskey(keys, keyname):
            keys[keyname] = self._getkeys_from_argskwds(args, kwds)
        for k, v in {**kwds, **keys}.items():
            self._parse_node_attrs(k, v, node_attrs, children_attrs)
        self._fix_key_if_invalid(node_attrs, parent, keyname)
        node_attrs['_keyname'] = keyname
        return node_attrs, children_attrs, keyname

    def _getkeys_from_argskwds(
            self,
            args: SectionKeysOrObjects,
            kwds: SectionAttrs
    ) -> SectionKeys:
        """
        Parse keys from args or kwds if it wasn't explicitly provided in kwds.
        """
        return (
            list(args)[0] if len(args) == 1 and not isinstance(
                args[0], list)
            else list(args) if len(args) >= 1
            else (  # no args supplied
                self.default_keyvalue if len(kwds) == 0  # no kwds supplied
                else self.default_keyvalue
            )
        )

    def _parse_node_attrs(
            self, name: str, value: Any, node_attrs: SectionAttrs,
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

    def _fix_key_if_invalid(
            self, attrs: SectionAttrs, parent: SectionParent, keyname: str
    ) -> None:
        """
        Enforce that node must have a keyname attr, and disallow key values
        from properties, callables.
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
    ) -> Section:
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
            self,
            node: Section,
            args: SectionKeysOrObjects,
            children_attrs: SectionAttrs,
            keyname: str
    ) -> None:
        """
        Recursively repeat construction per child with extracted child attrs.
        """
        nofchildren_from_attrs, children_from_args = (
            self._get_children_data(node, args, children_attrs))
        for child in children_from_args:
            node[getattr(child, keyname)] = child
        for i in range(nofchildren_from_attrs):
            child_attrs = {}
            for k, v in children_attrs.items():
                if len(v) > i:
                    child_attrs[k] = v[i]
            key = child_attrs.get(keyname, i)
            child_attrs[keyname] = key
            child = self._get_dictval_i(node, i)
            if child is None:
                child = node.__class__(parent=node, **child_attrs)
            node[getattr(child, keyname)] = child

    def _get_children_data(
            self,
            node: Section,
            args: SectionKeysOrObjects,
            attrs: SectionAttrs
    ) -> Tuple[int, List[Section]]:
        """
        Return number of children nodes implied by provided self.__call__ kwds,
        and any pre-constructed Section children passed in self.__call__ args.
        """
        nofchildren_from_attrs = (
            max(self._len(v) for v in attrs.values()) if attrs else 0)
        children_from_args = []
        for arg in args:
            from . import Section
            if isinstance(arg, Section):
                children_from_args += [arg]
        return (nofchildren_from_attrs, children_from_args)

    ##########################################################################
    #                              Utilities                                 #

    def _len(self, x: Any) -> int:
        """Return len of x if it is iterable, else 0."""
        return max(1, len(x)) if isinstance(x, list) else 0

    def _dict_haskey(self, d: AnyDict, key: Any) -> bool:
        "Return True if dict contains user-provided value for key, else False."
        return d.get(key, MetaSection._None) is not MetaSection._None

    def _get_dictval_i(self, d: AnyDict, i: int) -> Any:
        """Get value in iterator position i from dict as if its a list."""
        ret = None
        for ii, value in enumerate(d.values()):
            if ii == i:
                ret = value
                break
        return ret


class Section(dict, metaclass=MetaSection):
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

    _None = MetaSection._None
    _pluralizer = Pluralizer()
    _plurals = {}
    _singulars = {}
    _setattr_invalidate_cache_excludes = [
        'default_gettype',
        'use_cache',
    ]

    ##########################################################################
    #                                  init                                  #

    def __init__(self, **kwds: SectionAttrs) -> None:
        """Set object attr for every attr in kwds and init attr cache."""
        if self.use_cache and self.isleaf:
            self._cache = {}
        for name, value in kwds.items():
            self.__setattr__(name, value, _invalidate_cache=False)

    ##########################################################################
    #                  tree structure node access and info                   #

    @property
    def cls(self) -> Type[Section]:
        """The unique structure-wide class of each node."""
        return self.__class__

    @ property
    def nofchildren(self) -> int:
        """Nunber of children Sections/nodes."""
        return len(self)

    @ property
    def isroot(self, ) -> bool:
        """True iff self node has not parent."""
        return self.parent is None

    @ property
    def ischild(self, ) -> bool:
        """True iff self node has a parent."""
        return self.parent is not None

    @ property
    def isparent(self, ) -> bool:
        """True iff self node has any children."""
        return self.nofchildren > 0

    @ property
    def isleaf(self, ) -> bool:
        """True iff self node has no children."""
        return self.nofchildren == 0

    @ property
    def children(self) -> Section:
        """
        Get self nodes's children.
        Returns a Section node that has no public attrs and has shallow copies
        of self node's children as its children. This can be useful if self has
        an attr `attr` but you want to access a list of the childrens' attr
        `attr`, then write section.children.attr to access the attr list.
        """
        node = self.cls()
        node.update(self)
        setattr(node, node._keyname, self._None)
        return node

    @ property
    def sections(self) -> Section:
        """A synonym for property :meth:`children <Section.children>`."""
        return self.children

    @ property
    def leaves_iter(self) -> iter:
        """
        Return iterator that iterates through all self's leaf node descendants.
        """
        return (chain(*(child.leaves_iter for child in self.values()))
                if self.isparent else repeat(self, 1))

    @ property
    def leaves(self) -> Section:
        """
        Get all leaf node descendants of self.
        Returns a Section node that has no public attrs and has shallow copies
        of self node's leaves as its children. This can be useful if self has
        an attr `attr` but you want to access a list of the leaves' attr
        `attr`, then write section.leaves.attr to access the leaf attr list.
        """
        return self.node_withchildren_fromiter(self.leaves_iter)

    @ property
    def entries(self) -> Section:
        """A synonym for property :meth:`leaves <Section.leaves>`."""
        return self.leaves

    def node_withchildren_fromiter(self, itr: iter) -> Section:
        """
        Perform a general form of the task performed in
        :meth:`leaves <Section.leaves>`. Return a Section node with any
        children referenced in the iterable from the `itr` argument.
        """
        node = self.cls()
        for leaf in itr:
            node[getattr(leaf, self._keyname)] = (leaf)
        setattr(node, node._keyname, self._None)
        return node

    ##########################################################################
    #                      Attribute access/modification                     #

    def _invalidate_cache(self, name: Optional[str] = None) -> None:
        """
        Empty descendant attribute cache entirely or just for attribute `name`
        for self node and all parent nodes until root. This should be done
        every time a node is added or removed from the tree, or when a node
        attribute is changed.
        """
        node = self
        while node:
            if node.use_cache and not node.isleaf:
                if name:
                    plural, singular = self._get_plural_singular(name)
                    node._cache.pop(name, None)
                    node._cache.pop(plural, None)
                    node._cache.pop(singular, None)
                else:
                    node.__setattr__('_cache', {}, _invalidate_cache=False)
            node = node.parent

    def __setattr__(
            self, name: str, value: Any, _invalidate_cache=True
    ) -> None:
        """
        If value is a list, recursively
        setattr for each child node with the corresponding value element from
        the value list.
        """
        if isinstance(value, list):
            for child, v in zip(self.values(), value):
                setattr(child, name, v)
        else:
            super().__setattr__(name, value)
            if (_invalidate_cache and name[0] != '_' and not
                    self.cls._setattr_invalidate_cache_excludes.count(name)):
                self._invalidate_cache(name)

    def __getattr__(self, name: str) -> Any:
        """
        Called if self node does not have attribute `name`, in which case try
        finding attribute `name` from :meth:`__call__ <Section.__call__>`.
        """
        return self.__call__(name)

    def __call__(
            self,
            name: str,
            gettype: GetType = 'default'
    ) -> Union[Any, List[Any]]:
        """
        Run :meth:`get_nearest_attr <Section.get_nearest_attr>`. This returns
        attribute `name` from self if self contains the attribute in either the
        singular or plural form for `name`. Else, try the same pattern for each
        of self's children, putting the returned results from each child into a
        list. Else, raise AttributeError.

        :param name: The name of the attribute to find in self or self's
                     descendants

        :param gettype: Valid values are `'default'`, `'hybrid'` `list`,
                        `iter`, `dict`, `'full_dict'`.
                        Setting to `'default'` uses the value of
                        self.default_gettype for gettype.
                        Setting to `'hybrid'` returns a list if more than 1
                        element is found, else returns the non-iterable raw
                        form of the element.
                        Setting to `list` returns a list containing the
                        attribute values.
                        Setting to `iter` returns an iterable iterating
                        through the attribute
                        values. Setting to `dict` returns a dict containing
                        pairs of the
                        containing node's name with the attribute value.
                        Setting to
                        `'full_dict'` is faster than `dict` and returns a
                        dict containing pairs
                        of a reference to each node and its attribute value.
                        `'full_dict'`
                        output is visually identical to `dict` for printing
                        purposes, but it
                        will contain all attributes even if some source nodes
                        have duplicate
                        names. The only downside to `'full_dict'` that the
                        keys cannot be
                        referenced by name like with `dict`, but all values()
                        are still valid.

        :return: The attribute `name` of self if present, else an iterable
                 object containing the attribute `name` formed from the nearest
                 relatives of self. The type of the iterable object depends
                 on `gettype`.
        """
        return self.get_nearest_attr(name, gettype=gettype)

    def get_nearest_attr(
            self, name: str, gettype: GetType = 'default',
    ) -> Union[Any, List[Any], Iterable[Any], AnyDict]:
        """
        Default method called by :meth:`__call__ <Section.__call__>`. See
        the docstring of :meth:`__call__ <Section.__call__>` for the full
        details. :meta private:
        """
        attrs = self._get_nearest_attr(name)
        return self._parse_top_getattr(name, attrs, gettype=gettype)

    def _get_nearest_attr(
            self, name: str,
    ) -> Union[List[Any], Iterable[Any], AnyDict]:
        """
        Internal recursively called method for performing
        :meth:`get_nearest_attr <Section.get_nearest_attr>`.
        This method performs the same task as get_nearest_attr, except that the
        returned attributes are always in a `full_dict`.
        """
        attrs = self.__dict__.get(name, self._None)
        if attrs is self._None and self.use_pluralsingular:
            plural, singular = self._get_plural_singular(name)
            attrs = self.__dict__.get(plural, self._None)
        if attrs is self._None and self.use_pluralsingular:
            attrs = self.__dict__.get(singular, self._None)
        if attrs is not self._None:
            return {self: attrs}
        elif self.use_cache and not self.isleaf:
            attrs = self._cache.get(name, self._None)
        if attrs is self._None:
            attrs = {}
            for child in self.values():
                attrs.update(child._get_nearest_attr(name))
            if self.use_cache and not self.isleaf:
                self._cache[name] = attrs
        return attrs

    def _parse_top_getattr(
            self,
            name: str,
            attrs: Any,
            gettype: GetType = 'default',
    ) -> Union[Any, List[Any], Iterable[Any], AnyDict]:
        """
        Internal method for
        :meth:`get_nearest_attr <Section.get_nearest_attr>`.
        This method will return an iterable of a
        type depending on :param gettype: if values from multiple nodes are
        returned from :meth:`_get_nearest_attr <Section._get_nearest_attr>`,
        else if one value is found (from the root caller node) then the raw
        value is returned (not in an iterable), else raise AttributeError if no
        values are found.
        """
        if not len(attrs):
            raise AttributeError(name)
        if gettype == 'default':
            gettype = self.default_gettype
        if gettype is list or gettype == 'hybrid':
            attrs = list(attrs.values())
            if len(attrs) == 1 and gettype == 'hybrid':
                attrs = attrs[0]
        elif gettype is dict:
            attrs = eval(repr(attrs))
        elif gettype is iter:
            attrs = attrs.values()
        return attrs

    def get_node_attr(self, name: str, gettype: GetType = 'default') -> Any:
        """
        Return attribute `name` only from self as opposed to searching for
        attribute `attr` in descendant nodes as well.
        """
        attr = {self: self.__dict__.get(name, self._None)}
        return self._parse_top_getattr(name, attr, gettype=gettype)

    def _get_plural_singular(self, name: str) -> Tuple[str, str]:
        """
        Compute the plural and singular forms of `name` and store the
        results in a dict because calculating them repeatedly can be
        computationally expensive. The dicts are structure-wide attributes
        common to all nodes in a structure.
        """
        plural = self._plurals.get(name)
        singular = self._singulars.get(name)
        if not plural:
            plural = self._pluralizer.plural(name)
            self._plurals[singular] = plural
            self._plurals[plural] = plural
            self._plurals[name] = plural
        if not singular:
            singular = self._pluralizer.singular(name)
            self._singulars[singular] = singular
            self._singulars[plural] = singular
            self._singulars[name] = singular
        return plural, singular

    ##########################################################################
    #                           misc overrides                               #

    def __hash__(self) -> int:
        """
        Allows Section objects to be hashable, used in
        :meth:`get_nearest_attr <Section.get_nearest_attr` to keep a dict of
        which node every attr came from, even if nodes share the same name.
        """
        return hash(id(self))

    def __eq__(self, x: Any) -> bool:
        """For making Section objects be hashable."""
        return id(self) == id(x)

    def __ne__(self, x: Any) -> bool:
        """For making Section objects be hashable."""
        return id(self) != id(x)

    def __bool__(self) -> bool:
        """
        For convenience when checking if a node reference is valid or None.
        """
        return True

    def update(self, *args: Any, **kwds: Any) -> None:
        """
        Invalidate descendant attr cache after adding/removing nodes.
        :meta private:
        """
        self._invalidate_cache()
        super().update(*args, **kwds)

    def setdefault(self, *args: Any, **kwds: Any) -> Any:
        """Not supported yet. :meta private:"""
        raise NotImplementedError(
            'Section.setdefault() is not yet implemented.'
        )

    def pop(self, name: Any) -> Any:
        """ Remove child `name` from self. """
        self._invalidate_cache()
        return super().pop(name)

    def popitem(self) -> Tuple[Any, Any]:
        """Remove last added child from self."""
        self._invalidate_cache()
        return super().popitem()

    def __iter__(self) -> Iterable[Section]:
        """
        By default iterate over child nodes instead of their names/keys.
        """
        for v in self.values():
            yield v

    def __getitem__(self, name: Any) -> Section:
        """ Return child node `name` of self. """
        return super().__getitem__(name)

    def __setitem__(self, name: Any, value: Union[Section, AnyDict]) -> None:
        """
        Add a child `name` to self. Ensure added children are converted to the
        same unique Section type as the rest of the nodes in the structure, and
        update its name to `name`, and its parent to self.
        """
        assert name.__hash__
        from . import Section
        if isinstance(value, Section):
            if isinstance(value, self.cls):
                child = value
                child.__setattr__('parent', self, _invalidate_cache=False)
                child.__setattr__(child._keyname, name,
                                  _invalidate_cache=False)
            else:
                attrs = {k: v for k, v in value.__dict__.items()
                         if k[0] != '_'}
                attrs.pop(value._keyname, None)
                child = self.cls(name, **{**attrs, 'parent': self})
        elif isinstance(value, dict):
            child = self.cls(name, **{**value, 'parent': self})
        else:
            raise ValueError
        super().__setitem__(name, child)
        self._invalidate_cache()

    ##########################################################################
    #                         string representation                          #

    @property
    def _name(self) -> str:
        """
        Easily get the name/key of self node. This is slightly non-trivial
        because the name of the attribute representing the nodes name/key is
        contained in self._keyname and may be user-customizable in the future.
        """
        return getattr(self, self._keyname)

    def __str__(self) -> str:
        """Return self._name by default when printing self. Use
        :meth:`node_str <Section.node_str>` or
        :meth:`deep_str <Section.deep_str>` for printing a
        more detailed view of the node or entire structure."""
        return str(self._name)

    def __repr__(self) -> str:
        """
        For use in :meth:`_parse_top_getattr <Section._parse_top_getattr>`.
        Allows a dict with Section keys to easily be converted to a dict
        with node names as keys instead so that the values can actually be
        accessed through the names.

        TODO: A better approach not using repr for this will likely need to be
        implemented for the above in the future so that a valid repr string can
        be returned when used for other uses.
        """
        return "'" + str(self._name) + "'"

    def node_str(self) -> str:
        """
        Neatly print the public attributes of the Section node and its class,
        as well as its types property output.
        """
        s = ''
        other_params = {
            str(self.cls): self._node_types,
            'children': (list(self.keys())),
        }
        if self.isleaf:
            other_params.pop('children')
        do_repr = False
        attrs = {k: v for k, v in self.__dict__.items() if k[0] != '_'}
        attrs.pop(self._keyname, None)
        attrs = {**other_params, **{self._keyname: str(self._name)}, **attrs}
        for key, value in attrs.items():
            if isinstance(value, Section):
                value = str(value._name)
            if self.isroot and key == 'parent':
                continue
            final_keylen = 30
            prev_keylen = len(key)
            space = ' ' * max(final_keylen - prev_keylen, 0)
            value = repr(value) if do_repr else str(value)
            s += f'{key}{space}: ' + value + '\n'
            do_repr = True
        return s

    def deep_str(
            self, breadthfirst: bool = True, _topcall: bool = True
    ) -> str:
        """
        Print the output of :meth:`node_str <Section.node_str` for self and all
        of its descendants.
        """
        s = ''
        if _topcall:
            s += '#'*79 + '\n'
            if breadthfirst:
                s += self.node_str()
        if breadthfirst:
            for key, child in self.items():
                s += child.node_str()
        else:
            s += self.node_str()
        for child in self.values():
            s += child.deep_str(breadthfirst, _topcall=False)
        if _topcall:
            s += '#'*79 + '\n'
        return s

    @property
    def _node_types(self) -> str:
        """Return info about the position of self node in the structure."""
        s = ''
        divider = ', '
        if self.isroot:
            s += 'root' + divider
        if self.ischild:
            s += 'child' + divider
        if self.isparent:
            s += 'parent' + divider
        if self.isleaf:
            s += 'leaf' + divider
        return s[:-len(divider)]
