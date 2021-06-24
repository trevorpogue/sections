[ s e | c t | i o | n s ]
==============================

.. start-badges

|version| |supported-versions|

.. |version| image:: https://img.shields.io/pypi/v/sections.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/sections

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sections.svg
    :alt: Supported versions
    :target: https://pypi.org/project/sections

.. end-badges

Flexible tree data structures for organizing lists and dicts into sections.

`sections` is designed to be:

* **Intuitive**: Start quickly and spend less time reading the docs.
* **Scalable**: Grow arbitrarily complex trees as your problem scales.
* **Flexible**: Rapidly build nodes with any custom attributes, properties, and methods on the fly.
* **Fast**: Made with performance in mind - access lists and sub-lists/dicts in as little as Θ(1) time in many cases. See the Performance section for the full details.
* **Reliable**: Contains an exhaustive test suite and 100\% code coverage.

See the GitHub page at: https://github.com/trevorpogue/sections

=========================
Usage
=========================

.. code-block:: bash

    pip install sections

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-usage
                    :end-before: sphinx-end-usage
                    :dedent: 4


----------------------------------------------------------------
Attrs: Plural/singular hybrid attributes and more
----------------------------------------------------------------

Spend less time deciding between using the singular or plural form for an attribute name:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-plural-singular
                    :end-before: sphinx-end-plural-singular
                    :dedent: 4

When an attribute is not found in a Section node, both the plural and singular forms of the word are then checked to see if the node contains the attribute under those forms of the word. If they are still not found, the node will recursively repeat the same search on each of its children, concatenating the results into a list or dict.

--------------------------------------------------------------------
Properties: Easily add on the fly
--------------------------------------------------------------------

Properties and methods are automatically added to a Section class instance when passed as keyword arguments:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-properties
                    :end-before: sphinx-end-properties
                    :dedent: 4

Each sections() call returns a structure containing nodes of a unique class created in a factory function, where the class definition contains no logic except that it inherits from the Section class. This allows properties added to one structure creation to not affect the class instances in other structures.

--------------------------------------------------------------------
Construction: Build gradually or all at once
--------------------------------------------------------------------

Construct section-by-section, section-wise, attribute-wise, or other ways:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-books-construction
                    :end-before: sphinx-end-books-construction
                    :dedent: 4

=============
Details
=============

--------------
Section names
--------------

The non-keyword arguments passed into a sections() call define the section names and are accessed through the attribute `name`. The names are used like `keys` in a `dict` to access each child section of the root Section node:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-names
                    :end-before: sphinx-end-names
                    :dedent: 4

Names are optional, and by default, children will be given integer values corresponding to indices in an array, while a root has a default keyvalue of sections.NoneValue:

.. code-block:: python

    sect = sections(x=['a', 'b'])
    assert sect.sections.names == [0, 1]
    assert sect.name is sections.NoneValue

    # the string representation of sections.NoneValue is 'section'
    assert str(sect.name) == 'section'

---------------------------------
Parent names and attributes
---------------------------------

A parent section name can optionally be provided as the first argument in a list or Section instantiation by defining it in a set (surrounding it with curly brackets). This strategy avoids an extra level of braces when instantiating Sections. This idea applies also for defining parent attributes:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-parent-names
                    :end-before: sphinx-end-parent-names
                    :dedent: 4

-----------------------------------------------
Return attributes as a list, dict, or iterable
-----------------------------------------------

Access the data in different forms with the `gettype` argument in Sections.__call__() as follows:

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

See the __call__ method in the References section of the docs for more options: https://sections.readthedocs.io/

Set the default return type when accessing structure attributes by changing `Section.default_gettype` as follows:

.. code-block:: python

    menu = sections('Breakfast', 'Dinner', sides=['HashBrown', 'Fries'])

    menu['Breakfast'].default_gettype = dict  # set for only 'Breakfast' node
    assert menu.sides == ['HashBrown', 'Fries']
    assert menu['Breakfast']('side') == {'Breakfast': 'HashBrown'}

    menu.cls.default_gettype = dict           # set for all nodes in `menu`
    assert menu('sides') == {'Breakfast': 'HashBrown', 'Dinner': 'Fries'}
    assert menu['Breakfast']('side') == {'Breakfast': 'HashBrown'}

    sections.Section.default_gettype = dict  # set for all structures
    tasks1 = sections('pay bill', 'clean', status=['completed', 'started'])
    tasks2 = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks1('statuses') == {'pay bill': 'completed', 'clean': 'started'}
    assert tasks2('statuses') == {'pay bill': 'completed', 'clean': 'started'}

The above will also work for accessing attributes in the form `object.attr` but only if the node does not contain the attribute `attr`, otherwise it will return the non-iterable raw value for `attr`. Therefore, for consistency, access attributes using Section.__call__() like above if you wish to **always receive an iterable** form of the attributes.

--------------
Printing
--------------

Section structures can be visualized through the Section.deep_str() method as follows:


.. code-block:: python

    menu = sections(
        'Breakfast', 'Dinner',
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )
    print(menu.deep_str())

Output:

.. code-block:: python

    ###############################################################################
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: root, parent
    children                      : ['Breakfast', 'Dinner']
    name                          : 'section'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, leaf
    name                          : 'Breakfast'
    parent                        : 'section'
    mains                         : 'Bacon&Eggs'
    sides                         : 'HashBrown'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, leaf
    name                          : 'Dinner'
    parent                        : 'section'
    mains                         : 'Burger'
    sides                         : 'Fries'
    ###############################################################################

See the References section of the docs for more printing options: https://sections.readthedocs.io/.

--------------
Subclassing
--------------

Inheriting Section is easy, the only requirement is to call super().__init__(\*\*kwds) at some point in `__init__`  like below if you override that method:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-subclassing
                    :end-before: sphinx-end-subclassing
                    :dedent: 4

Section.__init__() assigns the kwds values passed to it to the object attributes, and the passed kwds are generated during instantiation by a metaclass.

--------------
Performance
--------------

Each non-leaf Section node keeps a cache containing quickly readable references to an attribute dict previously parsed from manual traversing through descendant nodes in a previous read. The caches are invalidated accordingly when the tree structure or node attribute values change. The caches allow instant reading of sub-lists/dicts in Θ(1) time and can often make structure attribute reading faster by 5x and even much more. The downside is that it also increases memory usage by roughly 5x as well. This is not a concern on a general-purpose computer for structures containing less than 1000 - 10,000 nodes. For clarity, converting a list with 10,000 elements would create 10,001 nodes (1 root plus 10,000 children). After 1000 - 10,000 nodes, it may be recommended to consider changing the node or structure's class attribute `use_cache` to `False`. This can be done as follows:


.. code-block:: python

    sect = sections([[[[[42] * 10] * 10] * 10] * 10])
    sect.use_cache = False              # turn off for just the root node
    sect.cls.use_cache = False          # turn off for all nodes in `sect`
    sections.Section.use_cache = False  # turn off for all structures

The dict option for `gettype` in the Section.__call__() method is currently slower than the other options. For performance-critical uses, if a dict is required just for visual printing purposes, it is recommended to use the faster 'full_dict' option for `gettype` instead of dict. See the Section.__call__() method in the References section of the docs for more details on the `gettype` options.
