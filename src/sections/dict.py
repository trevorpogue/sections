from typing import Any
from typing import Iterable
from typing import Tuple
from typing import Union

from .types import AnyDict
from .types import SectionType


class Dict:
    """Section dict overrides."""

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

    def _update(self, *args: Any, **kwds: Any) -> None:
        """
        Invalidate descendant attr cache after adding/removing nodes.
        """
        self._invalidate_caches()
        super().update(*args, **kwds)

    def items(self) -> Tuple[Iterable[Any], Iterable[Any]]:
        """Return iterator over child names and children."""
        return super().items()

    def keys(self) -> Iterable[Any]:
        """Return iterator over child names."""
        return super().keys()

    def values(self) -> Iterable[Any]:
        """Return iterator over chilren."""
        return super().values()

    def update(self, *args: Any, **kwds: Any) -> None:
        """Not supported."""
        raise NotImplementedError(
            'Section.update() is not implemented.'
        )

    def get(self, *args: Any, **kwds: Any) -> None:
        """Not supported."""
        raise NotImplementedError(
            'Section.get() is not implemented.'
        )

    def fromkeys(self, *args: Any, **kwds: Any) -> None:
        """Not supported."""
        raise NotImplementedError(
            'Section.fromkeys() is not implemented.'
        )

    def clear(self) -> None:
        """Not supported."""
        raise NotImplementedError(
            'Section.clear() is not implemented.'
        )

    def copy(self) -> None:
        """Not supported."""
        raise NotImplementedError(
            'Section.copy() is not implemented.'
        )

    def setdefault(self, *args: Any, **kwds: Any) -> Any:
        """Not supported."""
        raise NotImplementedError(
            'Section.setdefault() is not implemented.'
        )

    def pop(self, name: Any) -> Any:
        """Remove child `name` from self."""
        self._invalidate_caches()
        return super().pop(name)

    def popitem(self) -> Tuple[Any, Any]:
        """Remove last added child from self."""
        self._invalidate_caches()
        return super().popitem()

    def __iter__(self) -> Iterable[SectionType]:
        """
        By default iterate over child nodes instead of their names/keys.
        """
        for v in self.values():
            yield v

    def __getitem__(self, name: Any) -> SectionType:
        """Return child node `name` of self."""
        return super().__getitem__(name)

    def __setitem__(
            self, name: Any, value: Union[SectionType, AnyDict]
    ) -> None:
        """
        Add a child `name` to self. Ensure added children are converted to the
        same unique Section type as the rest of the nodes in the structure, and
        update its name to `name`, and its parent to self.
        """
        assert name.__hash__
        from . import Section
        if isinstance(value, Section):
            child = self._convert_to_self_cls(name, value)
        elif isinstance(value, dict):
            child = self.cls(name, **{**value, 'parent': self})
        else:
            raise ValueError
        super().__setitem__(name, child)
        self._invalidate_caches()

    def _convert_to_self_cls(
            self, name: Any, value: SectionType
    ) -> None:
        """Ensure output is of self's unique Section class instance type."""
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
        return child
