from ast import literal_eval
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from .pluralizer import Pluralizer
from .types import AnyDict
from .types import GetType
from .types import SectionNone


class AttrParser:
    """Logic for setting and getting attrs from self or descendant nodes."""

    ##########################################################################
    #              tree-structure-wide attributes for every node             #
    _pluralizer = Pluralizer()

    _setattr_invalidate_cache_excludes = [
        'default_gettype',
        'use_cache',
    ]
    ##########################################################################

    def _invalidate_caches(self, name: Optional[str] = None) -> None:
        """
        Empty self and all ancestor attribute caches entirely or just for
        attribute `name`. This should be done every time a node is added or
        removed from the tree, or when a node attribute is changed.
        """
        node = self
        while node:
            if node.use_cache and not node.isleaf:
                node._invalidate_node_cache(name)
            node = node.parent

    def _invalidate_node_cache(self, name: Optional[str] = None) -> None:
        """Invalidate cache for only self node."""
        if name:
            plural, singular = self._pluralizer(name)
            self._cache.pop(name, None)
            self._cache.pop(plural, None)
            self._cache.pop(singular, None)
        else:
            self.__setattr__('_cache', {}, _invalidate_cache=False)

    def __setattr__(
            self, name: str, value: Any, _invalidate_cache=True
    ) -> None:
        """
        If value is a list, recursively setattr for each child node with the
        corresponding value element from the value list.
        """
        if isinstance(value, list):
            for child, v in zip(self.values(), value):
                setattr(child, name, v)
        else:
            self._set_node_attr(name, value, _invalidate_cache)

    def _set_node_attr(
            self, name: str, value: Any, _invalidate_cache=True
    ) -> None:
        """Set attr for only the self node."""
        super().__setattr__(name, value)
        if (_invalidate_cache and name[0] != '_' and not
                self.cls._setattr_invalidate_cache_excludes.count(name)):
            self._invalidate_caches(name)

    def __getattr__(self, name: str) -> Any:
        """
        Called if self node does not have attribute `name`, in which case try
        finding attribute `name` from :meth:`__call__ <Section.__call__>`.
        """
        return self.__call__(name)

    def get_nearest_attr(
            self, name: str, gettype: GetType = 'default',
    ) -> Union[Any, List[Any], Iterable[Any], AnyDict]:
        """
        Default method called by :meth:`__call__ <Section.__call__>`. See
        the docstring of :meth:`__call__ <Section.__call__>` for the full
        details of what this method does.
        """
        attrs = self._get_nearest_attr(name)
        return self._parse_top_getattr(name, attrs, gettype=gettype)

    def _get_nearest_attr(
            self, name: str,
    ) -> Union[List[Any], Iterable[Any], AnyDict]:
        """
        This method performs the same task as
        :meth:`get_nearest_attr <Section.get_nearest_attr>`, except that the
        returned attributes are always in a `full_dict`.
        """
        attrs = self._get_node_attr(name)
        if attrs is SectionNone:
            attrs = {}
            for child in self.values():
                attrs.update(child._get_nearest_attr(name))
            if self.use_cache and not self.isleaf:
                self._cache[name] = attrs
        return attrs

    def get_node_attr(self, name: str, gettype: GetType = 'default') -> Any:
        """
        Return attribute `name` only from self as opposed to searching for
        attribute `attr` in descendant nodes as well.
        """
        attr = self._get_node_attr(name)
        return self._parse_top_getattr(name, attr, gettype=gettype)

    def _get_node_attr(self, name: str) -> AnyDict:
        """
        Differs from :meth:`get_node_attr <Section.get_node_attr>`
        in that this method will always return found attributes in a dict form
        so that the source node is tracked.
        """
        attr = self.__dict__.get(name, SectionNone)
        attr = self._get_pluralsingular_node_attr(name, attr)
        if attr is not SectionNone:
            return {self: attr}
        elif self.use_cache and not self.isleaf:
            attr = self._cache.get(name, SectionNone)
        return attr

    def _get_pluralsingular_node_attr(self, name: str, attr: Any) -> AnyDict:
        """Try getting the plural/singular forms of the attribute name."""
        if attr is SectionNone and self.use_pluralsingular:
            plural, singular = self._pluralizer(name)
            attr = self.__dict__.get(plural, SectionNone)
        if attr is SectionNone and self.use_pluralsingular:
            plural, singular = self._pluralizer(name)
            attr = self.__dict__.get(singular, SectionNone)
        return attr

    def _parse_top_getattr(
            self,
            name: str,
            attrs: Any,
            gettype: GetType = 'default',
    ) -> Union[Any, List[Any], Iterable[Any], AnyDict]:
        """
        Return an iterable of a type depending on argument
        `gettype` if values from multiple nodes are returned from
        :meth:`_get_nearest_attr <Section._get_nearest_attr>`, else if one
        value is found (from the root caller node) then the raw value is
        returned (not in an iterable), else raise AttributeError if no values
        are found.
        """
        _check_for_attribute_arror(name, attrs, gettype=gettype)
        if gettype == 'default':
            gettype = self.default_gettype
        if gettype == 'hybrid':
            return (list(attrs.values()) if len(attrs) > 1
                    else next(iter(attrs.values())))  # return dict value[0]
        else:
            return _get_iterable_attrs(attrs, gettype=gettype)


def _check_for_attribute_arror(
        name: str, attrs: AnyDict, gettype: GetType = 'default'
) -> None:
    """
    Raise attribute error if none were found.
    """
    if attrs is SectionNone or not len(attrs):
        raise AttributeError(name)


def _get_iterable_attrs(
        attrs: AnyDict, gettype: GetType = 'default',
) -> AnyDict:
    """
    Convert attrs from a dict to possibly a different requested iterable.
    """
    if gettype is list:
        attrs = list(attrs.values())
    elif gettype is dict:
        attrs = literal_eval(repr(attrs))
    elif gettype is iter:
        attrs = attrs.values()
    return attrs
