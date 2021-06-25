from itertools import chain
from itertools import repeat

from .types import SectionNone
from .types import SectionType


class Node:
    """Generic tree-structure node-related logic."""

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
    def children(self) -> SectionType:
        """
        Get self nodes's children. Returns a Section node that has no public
        attrs and has shallow copies of self node's children as its children.
        This can be useful if self has an attr `attr` but you want to access a
        list of the childrens' attr `attr`, then write section.children.attr to
        access the attr list.
        """
        node = self.cls()
        node._update(self)
        setattr(node, node._keyname, SectionNone)
        return node

    @ property
    def leaves_iter(self) -> iter:
        """
        Return iterator that iterates through all self's leaf node descendants.
        """
        return (chain(*(child.leaves_iter for child in self.values()))
                if self.isparent else repeat(self, 1))

    @ property
    def leaves(self) -> SectionType:
        """
        Get all leaf node descendants of self. Returns a Section node that has
        no public attrs and has shallow copies of self node's leaves as its
        children. This can be useful if self has an attr `attr` but you want to
        access a list of the leaves' attr `attr`, then write
        section.leaves.attr to access the leaf attr list.
        """
        return self.node_withchildren_fromiter(self.leaves_iter)

    def node_withchildren_fromiter(self, itr: iter) -> SectionType:
        """
        Perform a general form of the task performed in
        :meth:`leaves <Section.leaves>`. Return a Section node with any
        children referenced in the iterable from the `itr` argument.
        """
        node = self.cls()
        for leaf in itr:
            node[getattr(leaf, self._keyname)] = (leaf)
        setattr(node, node._keyname, SectionNone)
        return node
