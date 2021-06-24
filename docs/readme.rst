[ s e | c t | i o | n s ]
==============================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions|
        | |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/sections/badge/?style=flat
    :alt: Documentation Status
    :target: https://sections.readthedocs.io/

.. |travis| image:: https://api.travis-ci.com/trevorpogue/sections.svg?branch=main
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/trevorpogue/sections

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/trevorpogue/sections?branch=main&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/trevorpogue/sections

.. |requires| image:: https://requires.io/github/trevorpogue/sections/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/trevorpogue/sections/requirements/?branch=main

.. |coveralls| image:: https://coveralls.io/repos/github/trevorpogue/sections/badge.svg
    :alt: Coverage Status
    :target: https://coveralls.io/github/trevorpogue/sections

.. |codecov| image:: https://codecov.io/gh/trevorpogue/sections/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/trevorpogue/sections

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/92804e7a0df44f09b42bc6ee1664bc67
    :alt: Codacy Code Quality Status
    :target: https://www.codacy.com/gh/trevorpogue/sections/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=trevorpogue/sections&amp;utm_campaign=Badge_Grade

.. |codeclimate| image:: https://codeclimate.com/github/trevorpogue/sections/badges/gpa.svg
   :alt: CodeClimate Quality Status
   :target: https://codeclimate.com/github/trevorpogue/sections

.. |version| image:: https://img.shields.io/pypi/v/sections.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/sections

.. |wheel| image:: https://img.shields.io/pypi/wheel/sections.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/sections

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sections.svg
    :alt: Supported versions
    :target: https://pypi.org/project/sections

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sections.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/sections

.. |commits-since| image:: https://img.shields.io/github/commits-since/trevorpogue/sections/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/trevorpogue/sections/compare/v0.0.0...main


.. |scrutinizer| image:: https://scrutinizer-ci.com/g/trevorpogue/sections/badges/quality-score.png?b=main
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/trevorpogue/sections/

.. end-badges

Flexible tree data structures for organizing lists and dicts into sections.

``sections`` is designed to be:

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

If you don't like this feature, simply turn it off as shown in the **Detail - Attribute access** section.

--------------------------------------------------------------------
Properties: Easily add on the fly
--------------------------------------------------------------------

Properties and methods are automatically added to all nodes in a structure returned from a ``sections()`` call when passed as keyword arguments:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-properties
                    :end-before: sphinx-end-properties
                    :dedent: 4

Each call returns a structure containing nodes of a unique class created in a class factory function, where the unique class definition contains no logic except that it inherits from the Section class. This allows properties/methods added to one structure's class definition to not affect the class definitions of nodes from other structures.

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

----------------------------------------------------------------
Attribute access
----------------------------------------------------------------

Recap: spend less time deciding between using the singular or plural form for an attribute name:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-plural-singular
                    :end-before: sphinx-end-plural-singular
                    :dedent: 4

When an attribute is not found in a Section node, both the plural and singular forms of the word are then checked to see if the node contains the attribute under those forms of the word. If they are still not found, the node will recursively repeat the same search on each of its children, concatenating the results into a list or dict. The true attribute name in each node supplied a corresponding value is whatever name was given in the keyword argument's key (i.e. ``status`` in the above example).

If you don't like this feature, simply turn it off using the following:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-plural-singular-disable
                    :end-before: sphinx-end-plural-singular-disable
                    :dedent: 4

Note, however, that this will still traverse descendant nodes to see if they contain the requested attribute. To stop using this feature also, access attributes using the get_node_attr_ method instead.

--------------
Section names
--------------

The non-keyword arguments passed into a ``sections()`` call define the section names and are accessed through the attribute ``name``. The names are used like ``keys`` in a ``dict`` to access each child section of the root Section node:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-names
                    :end-before: sphinx-end-names
                    :dedent: 4

Names are optional, and by default, children will be given integer values corresponding to indices in an array, while a root has a default keyvalue of ``sections.SectionNone``:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-names-printing
                    :end-before: sphinx-end-names-printing
                    :dedent: 4

---------------------------------
Parent names and attributes
---------------------------------

A parent section name can optionally be provided as the first argument in a list or Section instantiation by defining it in a set (surrounding it with curly brackets). This strategy avoids an extra level of braces when instantiating Section objects. This idea applies also for defining parent attributes:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-parent-names
                    :end-before: sphinx-end-parent-names
                    :dedent: 4

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

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-gettype
                    :end-before: sphinx-end-gettype
                    :dedent: 4

The above will also work for accessing attributes in the form ``object.attr`` but only if the node does not contain the attribute ``attr``, otherwise it will return the non-iterable raw value for ``attr``. Therefore, for consistency, access attributes using ``Section.__call__()`` like above if you wish to **always receive an iterable** form of the attributes.

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

Output:

.. code-block:: python

    ###############################################################################
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: root, parent
    children            : ['Fantasy', 'Academic']
    name                : "My Bookshelf"
    parent              : None
    topics              : 'All my books'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, parent
    children            : ['LOTR', 'Harry Potter']
    name                : 'Fantasy'
    parent              : "My Bookshelf"
    topics              : 'Imaginary things'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, parent
    children            : ['Advanced Mathematics', 'Physics for Engineers']
    name                : 'Academic'
    parent              : "My Bookshelf"
    topics              : 'School'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, leaf
    name                : 'LOTR'
    parent              : 'Fantasy'
    topics              : 'Hobbits'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, leaf
    name                : 'Harry Potter'
    parent              : 'Fantasy'
    topics              : 'Wizards'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, leaf
    name                : 'Advanced Mathematics'
    parent              : 'Academic'
    topics              : 'Numbers'
    <class 'sections.Sections.UniqueSection.<locals>.Section'>: child, leaf
    name                : 'Physics for Engineers'
    parent              : 'Academic'
    topics              : 'Forces'
    ###############################################################################

See the References_ section of the docs for more printing options.

--------------
Subclassing
--------------

Inheriting Section is easy, the only requirement is to call ``super().__init__(**kwds)`` at some point in ``__init__()``  like below if you override that method:

.. literalinclude:: ../tests/test_doc_examples.py
                    :start-after: sphinx-start-subclassing
                    :end-before: sphinx-end-subclassing
                    :dedent: 4

``Section.__init__()`` assigns the kwds values passed to it to the object attributes, and the passed kwds are generated during instantiation by a metaclass.

--------------
Performance
--------------

Each non-leaf Section node keeps a cache containing quickly readable references of attribute dicts previously parsed from manual traversing through descendant nodes in an earlier read. The caches are invalidated accordingly for modified nodes and their ancestors when the tree structure or node attribute values change. The caches allow instant reading of sub-lists/dicts in Θ(1) time and can often make structure attribute reading faster by 5x or even much more if the structure is rarely modified after creation. The downside is that it also increases memory usage by roughly 5x as well. This is not a concern on a general-purpose computer for structures containing less than 1000 - 10,000 nodes. For clarity, converting a list with 10,000 elements would create 10,001 nodes (1 root plus 10,000 children). However, for structure containing more than 1000 - 10,000 nodes, it may be recommended to consider changing the node or structure's class attribute ``use_cache`` to ``False``. This can be done as follows:

.. code-block:: python

    sect = sections([[[[[42] * 10] * 10] * 10] * 10])
    sect.use_cache = False              # turn off for just the root node
    sect.cls.use_cache = False          # turn off for all nodes in `sect`
    sections.Section.use_cache = False  # turn off for all structures

The dict option for ``gettype`` in the ``Section.__call__()`` method is
currently slower than the other options. For performance-critical uses, use the
other options for ``gettype``. Alternatively, if a dict is required just for
visual printing purposes, use the faster ``'full_dict'`` option for ``gettype``
instead. This option returns dicts with valid values with keys that have string
representations of the node names, but the keys are in reality references to
node objects and cannot be referenced by the user through strings.
See the ``Section.__call__()`` method in the References_ section of the docs for more details on the ``gettype`` options.

.. _References: https://sections.readthedocs.io/en/latest/reference/index.html

.. _get_node_attr: https://sections.readthedocs.io/en/latest/reference/index.html#sections.Section.get_node_attr
