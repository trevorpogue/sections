from typing import Any


class StringParser:
    """String parsing methods for visualizing nodes and structures."""

    @property
    def _name(self) -> str:
        """
        Easily get the name/key of self node. This is slightly non-trivial
        because the name of the attribute representing the nodes name/key is
        contained in self._keyname and may be user-customizable in the future.
        """
        return getattr(self, self._keyname)

    def __str__(self) -> str:
        """
        Return self._name by default when printing self. Use
        :meth:`node_str <Section.node_str>` or
        :meth:`deep_str <Section.deep_str>` for printing a
        more detailed view of the node or entire structure.
        """
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
        s = repr(self._name) + ' = <' + self._node_types + '>\n'
        other_params = {
            'parent': self._name,
            'children': (list(self.keys())),
        }
        if self.isleaf:
            other_params.pop('children')
        attrs = {k: v for k, v in self.__dict__.items() if k[0] != '_'}
        attrs = {**other_params, **{self._keyname: str(self._name)}, **attrs}
        attrs.pop(self._keyname, None)
        for name, value in attrs.items():
            s += self._parse_public_node_attrs(name, value)
        return s

    def _parse_public_node_attrs(self, name: Any, value: Any) -> str:
        from . import Section
        pad = ''
        if isinstance(value, Section):
            value = repr(value._name)
        else:
            value = str(value) if name == str(self.cls) else repr(value)
        return f'    {name}{pad} = ' + value + '\n'

    def deep_str(
            self, breadthfirst: bool = True
    ) -> str:
        """
        Print the output of :meth:`node_str <Section.node_str` for self and all
        of its descendants.

        :param breadthfirst: Set True to print descendants in a breadth-first
               pattern or False for depth-first.
        """
        s = '#' * 79 + '\n'
        s += '<class ' + repr(self.cls.__name__) + '> structure\n\n'
        if breadthfirst:
            s += self.node_str() + '\n'
        s += self._deep_str(breadthfirst=breadthfirst)[:-1]  # remove last '\n'
        s += '#' * 79 + '\n'
        return s

    def _deep_str(self, breadthfirst: bool = True) -> str:
        """
        Private recursive call for :meth:`deep_str <Section.deep_str`.
        """
        s = ''
        if breadthfirst:
            for child in self.values():
                s += child.node_str() + '\n'
        else:
            s += self.node_str() + '\n'
        for child in self.values():
            s += child._deep_str(breadthfirst=breadthfirst)
        return s

    @ property
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
