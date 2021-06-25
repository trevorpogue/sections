[ s e | c t | i o | n s ]
==============================

.. start-badges

|coveralls| |codacy| |codeclimate|

|version| |supported-versions| |supported-implementations| |wheel|

|requires| |commits-since| |docs|

|downloads| |downloads-week|

.. |coveralls| image:: https://coveralls.io/repos/github/trevorpogue/sections/badge.svg
    :alt: Coverage Status
    :target: https://coveralls.io/github/trevorpogue/sections

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/92804e7a0df44f09b42bc6ee1664bc67
    :alt: Codacy Code Quality Status
    :target: https://www.codacy.com/gh/trevorpogue/sections/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=trevorpogue/sections&amp;utm_campaign=Badge_Grade

.. |codeclimate| image:: https://codeclimate.com/github/trevorpogue/sections/badges/gpa.svg
   :alt: CodeClimate Quality Status
   :target: https://codeclimate.com/github/trevorpogue/sections

.. |version| image:: https://img.shields.io/pypi/v/sections.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/sections

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sections.svg
    :alt: Supported versions
    :target: https://pypi.org/project/sections

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sections.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/sections

.. |wheel| image:: https://img.shields.io/pypi/wheel/sections.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/sections

.. |downloads| image:: https://pepy.tech/badge/sections
    :alt: downloads
    :target: https://pepy.tech/project/sections

.. |downloads-week| image:: https://pepy.tech/badge/sections/week
    :alt: downloads
    :target: https://pepy.tech/project/sections

.. |docs| image:: https://readthedocs.org/projects/sections/badge/?style=flat
    :alt: Documentation Status
    :target: https://sections.readthedocs.io/

.. |requires| image:: https://requires.io/github/trevorpogue/sections/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/trevorpogue/sections/requirements/?branch=main

.. |commits-since| image:: https://img.shields.io/github/commits-since/trevorpogue/sections/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/trevorpogue/sections/compare/v0.0.0...main

.. end-badges

Flexible tree data structures for organizing lists and dicts into sections.

``sections`` is designed to be:

* **Intuitive**: Start quickly and spend less time reading the docs.
* **Scalable**: Grow arbitrarily complex trees as your problem scales.
* **Flexible**: Rapidly build nodes with any custom attributes, properties, and methods on the fly.
* **Fast**: Made with performance in mind - access lists and sub-lists/dicts in as little as Θ(1) time in many cases. See the Performance section for the full details.
* **Reliable**: Contains an exhaustive test suite and 100\% code coverage.

See the full documentation at: https://sections.readthedocs.io/

=========================
Usage
=========================

.. code-block:: bash

    pip install sections

.. code-block:: python

    import sections

    menu = sections(
        'Breakfast', 'Dinner',
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )
    # Resulting structure's API and the expected results:
    assert menu.mains == ['Bacon&Eggs', 'Burger']
    assert menu.sides == ['HashBrown', 'Fries']
    assert menu['Breakfast'].main == 'Bacon&Eggs'
    assert menu['Breakfast'].side == 'HashBrown'
    assert menu['Dinner'].main == 'Burger'
    assert menu['Dinner'].side == 'Fries'
    assert menu('sides', list) == ['HashBrown', 'Fries']
    assert menu('sides', dict) == {'Breakfast': 'HashBrown', 'Dinner': 'Fries'}
    # root section/node:
    assert isinstance(menu, sections.Section)
    # child sections/nodes:
    assert isinstance(menu['Breakfast'], sections.Section)
    assert isinstance(menu['Dinner'], sections.Section)


----------------------------------------------------------------
Attrs: Plural/singular hybrid attributes and more
----------------------------------------------------------------

Spend less time deciding between using the singular or plural form for an attribute name:

.. code-block:: python

    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks.statuses == ['completed', 'started']
    assert tasks['pay bill'].status == 'completed'
    assert tasks['clean'].status == 'started'

If you don't like this feature, simply turn it off as shown in the **Detail - Attribute access settings** section.

--------------------------------------------------------------------
Properties: Easily add on the fly
--------------------------------------------------------------------

Properties and methods are automatically added to all nodes in a structure returned from a ``sections()`` call when passed as keyword arguments:

.. code-block:: python

    schedule = sections(
        'Weekdays', 'Weekend',
        hours_per_day=[[8, 8, 6, 10, 8], [4, 6]],
        hours=property(lambda self: sum(self.hours_per_day)),
    )
    assert schedule['Weekdays'].hours == 40
    assert schedule['Weekend'].hours == 10
    assert schedule.hours == 50

Each call returns a structure containing nodes of a unique class created in a class factory function, where the unique class definition contains no logic except that it inherits from the Section class. This allows properties/methods added to one structure's class definition to not affect the class definitions of nodes from other structures.

--------------------------------------------------------------------
Construction: Build gradually or all at once
--------------------------------------------------------------------

Construct section-by-section, section-wise, attribute-wise, or other ways:

.. code-block:: python

    def demo_different_construction_techniques():
        """Example construction techniques for producing the same structure."""

        # Building section-by-section
        books = sections()
        books['LOTR'] = sections(topic='Hobbits', author='JRR Tolkien')
        books['Harry Potter'] = sections(topic='Wizards', author='JK Rowling')
        demo_resulting_object_api(books)

        # Section-wise construction
        books = sections(
            sections('LOTR', topic='Hobbits', author='JRR Tolkien'),
            sections('Harry Potter', topic='Wizards', author='JK Rowling')
        )
        demo_resulting_object_api(books)

        # Attribute-wise construction
        books = sections(
            'LOTR', 'Harry Potter',
            topics=['Hobbits', 'Wizards'],
            authors=['JRR Tolkien', 'JK Rowling']
        )
        demo_resulting_object_api(books)

        # setattr post-construction
        books = sections(
            'LOTR', 'Harry Potter',
        )
        books.topics = ['Hobbits', 'Wizards']
        books['LOTR'].author = 'JRR Tolkien'
        books['Harry Potter'].author = 'JK Rowling'
        demo_resulting_object_api(books)

    def demo_resulting_object_api(books):
        """Example Section structure API and expected results."""
        assert books.names == ['LOTR', 'Harry Potter']
        assert books.topics == ['Hobbits', 'Wizards']
        assert books.authors == ['JRR Tolkien', 'JK Rowling']
        assert books['LOTR'].topic == 'Hobbits'
        assert books['LOTR'].author == 'JRR Tolkien'
        assert books['Harry Potter'].topic == 'Wizards'
        assert books['Harry Potter'].author == 'JK Rowling'

    demo_different_construction_techniques()

=============
Details
=============

--------------
Section names
--------------

The non-keyword arguments passed into a ``sections()`` call define the section names and are accessed through the attribute ``name``. The names are used like ``keys`` in a ``dict`` to access each child section of the root Section node:

.. code-block:: python

    books = sections(
        'LOTR', 'Harry Potter',
        topics=['Hobbits', 'Wizards'],
        authors=['JRR Tolkien', 'JK Rowling']
    )
    assert books.names == ['LOTR', 'Harry Potter']
    assert books['LOTR'].name == 'LOTR'
    assert books['Harry Potter'].name == 'Harry Potter'

Names are optional, and by default, children will be given integer values corresponding to indices in an array, while a root has a default keyvalue of ``sections.SectionNone``:

.. code-block:: python

    sect = sections(x=['a', 'b'])
    assert sect.sections.names == [0, 1]
    assert sect.name is sections.SectionNone

    # the string representation of sections.SectionNone is 'section':
    assert str(sect.name) == 'section'

---------------------------------
Parent names and attributes
---------------------------------

A parent section name can optionally be provided as the first argument in a list or Section instantiation by defining it in a set (surrounding it with curly brackets). This strategy avoids an extra level of braces when instantiating Section objects. This idea applies also for defining parent attributes:

.. code-block:: python

    library = sections(
        {"My Bookshelf"},
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Mathematics', 'Physics for Engineers'],
        topics=[{'All my books'},
                [{'Imaginary things'}, 'Hobbits', 'Wizards'],
                [{'School'}, 'Numbers', 'Forces']],
    )
    assert library.name == "My Bookshelf"
    assert library.sections.names == ['Fantasy', 'Academic']
    assert library['Fantasy'].sections.names == ['LOTR', 'Harry Potter']
    assert library['Academic'].sections.names == [
        'Advanced Mathematics', 'Physics for Engineers'
    ]
    assert library['Fantasy']['Harry Potter'].name == 'Harry Potter'
    assert library.topic == 'All my books'
    assert library['Fantasy'].topic == 'Imaginary things'
    assert library['Academic'].topic == 'School'

-----------------------------------------------
Return attributes as a list, dict, or iterable
-----------------------------------------------

Access the data in different forms with the ``gettype`` argument in ``Section.__call__()`` as follows:

.. code-block:: python

    menu = sections('Breakfast', 'Dinner', sides=['HashBrown', 'Fries'])

    # return as list always, even if a single element is returned
    assert menu('sides', list) == ['HashBrown', 'Fries']
    assert menu['Breakfast']('side', list) == ['HashBrown']

    # return as dict
    assert menu('sides', dict) == {'Breakfast': 'HashBrown', 'Dinner': 'Fries'}
    assert menu['Breakfast']('side', dict) == {'Breakfast': 'HashBrown'}

    # return as iterator over elements in list (fastest method, theoretically)
    for i, value in enumerate(menu('sides', iter)):
        assert value == ['HashBrown', 'Fries'][i]
    for i, value in enumerate(menu['Breakfast']('side', iter)):
        assert value == ['HashBrown'][i]

See the ``Section.__call__()`` method in the References_ section of the docs for more options.

Set the default return type when accessing structure attributes by changing ``Section.default_gettype`` as follows:

.. code-block:: python

    menu = sections('Breakfast', 'Dinner', sides=['HashBrown', 'Fries'])

    menu['Breakfast'].default_gettype = dict  # set for only 'Breakfast' node
    assert menu.sides == ['HashBrown', 'Fries']
    assert menu['Breakfast']('side') == {'Breakfast': 'HashBrown'}

    menu.cls.default_gettype = dict           # set for all nodes in ``menu``
    assert menu('sides') == {'Breakfast': 'HashBrown', 'Dinner': 'Fries'}
    assert menu['Breakfast']('side') == {'Breakfast': 'HashBrown'}

    sections.Section.default_gettype = dict   # set for all structures
    tasks1 = sections('pay bill', 'clean', status=['completed', 'started'])
    tasks2 = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks1('statuses') == {'pay bill': 'completed', 'clean': 'started'}
    assert tasks2('statuses') == {'pay bill': 'completed', 'clean': 'started'}

The above will also work for accessing attributes in the form ``object.attr`` but only if the node does not contain the attribute ``attr``, otherwise it will return the non-iterable raw value for ``attr``. Therefore, for consistency, access attributes using ``Section.__call__()`` like above if you wish **always receive an iterable** form of the attributes.

----------------------------------------------------------------
Attribute access settings
----------------------------------------------------------------

Recap: spend less time deciding between using the singular or plural form for an attribute name:

.. code-block:: python

    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks.statuses == ['completed', 'started']
    assert tasks['pay bill'].status == 'completed'
    assert tasks['clean'].status == 'started'

When an attribute is not found in a Section node, both the plural and singular forms of the word are then checked to see if the node contains the attribute under those forms of the word. If they are still not found, the node will recursively repeat the same search on each of its children, concatenating the results into a list or dict. The true attribute name in each node supplied a corresponding value is whatever name was given in the keyword argument's key (i.e. ``status`` in the above example).

If you don't like this feature, simply turn it off using the following:

.. code-block:: python

    import pytest
    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks.statuses == ['completed', 'started']
    sections.Section.use_pluralsingular = False  # turn off for all future objs
    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    with pytest.raises(AttributeError):
        tasks.statuses  # this now raises an AttributeError

Note, however, that this will still traverse descendant nodes to see if they
contain the requested attribute. To stop using this feature also, access
attributes using the `Section.get_node_attr()`_ method instead.

--------------
Printing
--------------

Section structures can be visualized through the ``Section.deep_str()`` method as follows:


.. code-block:: python

    library = sections(
        {"My Bookshelf"},
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Mathematics', 'Physics for Engineers'],
        topics=[{'All my books'},
                [{'Imaginary things'}, 'Hobbits', 'Wizards'],
                [{'School'}, 'Numbers', 'Forces']],
    )
    print(library.deep_str())

Output:

.. code-block:: python

    ###############################################################################
    <class 'Section'> structure

    'My Bookshelf' = <root, parent>
        parent = None
        children = ['Fantasy', 'Academic']
        topics = 'All my books'

    'Fantasy' = <child, parent>
        parent = 'My Bookshelf'
        children = ['LOTR', 'Harry Potter']
        topics = 'Imaginary things'

    'Academic' = <child, parent>
        parent = 'My Bookshelf'
        children = ['Advanced Mathematics', 'Physics for Engineers']
        topics = 'School'

    'LOTR' = <child, leaf>
        parent = 'Fantasy'
        topics = 'Hobbits'

    'Harry Potter' = <child, leaf>
        parent = 'Fantasy'
        topics = 'Wizards'

    'Advanced Mathematics' = <child, leaf>
        parent = 'Academic'
        topics = 'Numbers'

    'Physics for Engineers' = <child, leaf>
        parent = 'Academic'
        topics = 'Forces'
    ###############################################################################

See the References_ section of the docs for more printing options.

--------------
Subclassing
--------------

Inheriting Section is easy, the only requirement is to call ``super().__init__(**kwds)`` at some point in ``__init__()``  like below if you override that method:

.. code-block:: python

    class Library(sections.Section):
        def __init__(price="Custom default value", **kwds):
            super().__init__(**kwds)

        @property
        def genres(self):
            if self.isroot:
                return self.sections
            else:
                raise AttributeError('This library has only 1 level of genres')

        @property
        def books(self): return self.leaves

        @property
        def titles(self): return self.names

        def critique(self, impression="Haven't read it yet", rating=0):
            self.review = impression
            self.price = rating * 2

    library = Library(
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Math.', 'Physics for Engineers']
    )
    assert library.genres.names == ['Fantasy', 'Academic']
    assert library.books.titles == [
        'LOTR', 'Harry Potter', 'Advanced Math.', 'Physics for Engineers'
    ]
    library.books['LOTR'].critique(impression='Good but too long', rating=7)
    library.books['Harry Potter'].critique(
        impression="I don't like owls", rating=4)
    assert library.books['LOTR'].price == 14
    assert library.books['Harry Potter'].price == 8
    import pytest
    with pytest.raises(AttributeError):
        library['Fantasy'].genres

``Section.__init__()`` assigns the kwds values passed to it to the object attributes, and the passed kwds are generated during instantiation by a metaclass.

--------------
Performance
--------------

Each non-leaf Section node keeps a cache containing quickly readable references of attribute dicts previously parsed from manual traversing through descendant nodes in an earlier read. The caches are invalidated accordingly for modified nodes and their ancestors when the tree structure or node attribute values change.

The caches allow instant reading of sub-lists/dicts in Θ(1) time and can often make structure attribute reading faster by 5x or even much more once the structure is rarely being modified. The downside is that it also increases memory usage by roughly 5x as well. This is not a concern on a general-purpose computer for structures representing lists/dicts with less than 1000 - 10,000 elements. However, for structures in this range or larger, it is recommended to consider changing the node or structure's class attribute ``use_cache`` to ``False``. This can be done as follows:

.. code-block:: python

    sect = sections(*[[[42] * 10] * 10] * 10] * 10])
    sect.use_cache = False              # turn off for just the root node
    sect.cls.use_cache = False          # turn off for all nodes in `sect`
    sections.Section.use_cache = False  # turn off for all structures

The dict option for ``gettype`` in the ``Section.__call__()`` method is
currently slower than the other options. For performance-critical uses, use the
other options for ``gettype``.
Alternatively, if a dict is required just for
visual printing purposes, use the faster ``'full_dict'`` option for ``gettype``
instead. This option returns dicts with valid values with keys that have string
representations of the node names, but the keys are in reality references to
node objects and cannot be referenced by the user through strings.
See the ``Section.__call__()`` method in the References_ section of the docs for more details on the ``gettype`` options.

.. _References: https://sections.readthedocs.io/en/latest/reference/index.html
.. _Section.get_node_attr(): https://sections.readthedocs.io/en/latest/reference/#sections.Section.get_node_attr
