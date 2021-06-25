"""
Flexible tree data structures for organizing lists and dicts into sections.

https://github.com/trevorpogue/sections
"""

__version__ = '0.0.0'
__all__ = ['MetaSection', 'Section', 'SectionNone']

import sys
from typing import Type

from .meta import Meta as MetaSection
from .section import Section
from .types import SectionAttrs
from .types import SectionKeysOrObjects
from .types import SectionNone


class Sections:

    """Class form of sections module to make the module callable."""

    @property
    def UniqueSection(self) -> Type[Section]:
        """
        Return a unique class that inherits Section but can have its own
        unique properties and methods defined based on args/kwds, but will not
        influence these attributes in other classes returned from this method.
        """
        from .section import Section as _Section

        class Section(_Section):

            """Unique Section class creation."""

        return Section

    def __call__(
            self, *args: SectionKeysOrObjects, **kwds: SectionAttrs,
    ) -> Section:
        """
        Return a structure containing nodes all of the same unique Class
        instance type. And each structure returned will contain nodes with
        types of a different unique class instance than other structures.
        """
        return self.UniqueSection(*args, **kwds)


sections = Sections()

sys.modules['sections'] = sections  # make the module callable

# Add all the attributes to the 'module' so things can be imported normally
for key, value in list(globals().items()):
    if key in 'collections sys __VersionInfo key value config':
        # Avoid polluting the namespace
        continue

    setattr(sections, key, value)
