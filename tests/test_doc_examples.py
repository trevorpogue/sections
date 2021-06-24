import sections


def test_docs_examples_usage() -> None:
    # sphinx-start-usage
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
    # sphinx-end-usage

    # sphinx-start-plural-singular
    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks.statuses == ['completed', 'started']
    assert tasks['pay bill'].status == 'completed'
    assert tasks['clean'].status == 'started'
    # sphinx-end-plural-singular

    # sphinx-start-plural-singular-disable
    import pytest
    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks.statuses == ['completed', 'started']
    sections.Section.use_pluralsingular = False  # turn off for all future objs
    tasks = sections('pay bill', 'clean', status=['completed', 'started'])
    with pytest.raises(AttributeError):
        tasks.statuses  # this now raises an AttributeError
    # sphinx-end-plural-singular-disable
    sections.Section.use_pluralsingular = True  # set back

    # sphinx-start-properties
    schedule = sections(
        'Weekdays', 'Weekend',
        hours_per_day=[[8, 8, 6, 10, 8], [4, 6]],
        hours=property(lambda self: sum(self.hours_per_day)),
    )
    assert schedule['Weekdays'].hours == 40
    assert schedule['Weekend'].hours == 10
    assert schedule.hours == 50
    # sphinx-end-properties

    # sphinx-start-books-construction
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
    # sphinx-end-books-construction


def test_docs_examples_details() -> None:
    # In-Depth Tutorial

    # Sections Names
    # sphinx-start-names
    books = sections(
        'LOTR', 'Harry Potter',
        topics=['Hobbits', 'Wizards'],
        authors=['JRR Tolkien', 'JK Rowling']
    )
    assert books.names == ['LOTR', 'Harry Potter']
    assert books['LOTR'].name == 'LOTR'
    assert books['Harry Potter'].name == 'Harry Potter'
    # sphinx-end-names

    # sphinx-start-names-printing
    sect = sections(x=['a', 'b'])
    assert sect.sections.names == [0, 1]
    assert sect.name is sections.SectionNone

    # the string representation of sections.SectionNone is 'section':
    assert str(sect.name) == 'section'
    # sphinx-end-names-printing

    # Parent Names
    # sphinx-start-parent-names
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
    # sphinx-end-parent-names

    # Subclassing
    # sphinx-start-subclassing
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
    # sphinx-end-subclassing

    # sphinx-begin-getattr-options
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

    # See the __call__ method in the References section of the docs for more
    # options: https://sections.readthedocs.io/
    # sphinx-end-getattr-options

    # sphinx-begin-gettype
    menu = sections('Breakfast', 'Dinner', sides=['HashBrown', 'Fries'])

    menu['Breakfast'].default_gettype = dict  # set for only 'Breakfast' node
    assert menu.sides == ['HashBrown', 'Fries']
    assert menu['Breakfast']('side') == {'Breakfast': 'HashBrown'}

    menu.cls.default_gettype = dict           # set for all nodes in `menu`
    assert menu('sides') == {'Breakfast': 'HashBrown', 'Dinner': 'Fries'}
    assert menu['Breakfast']('side') == {'Breakfast': 'HashBrown'}

    sections.Section.default_gettype = dict   # set for all structures
    tasks1 = sections('pay bill', 'clean', status=['completed', 'started'])
    tasks2 = sections('pay bill', 'clean', status=['completed', 'started'])
    assert tasks1('statuses') == {'pay bill': 'completed', 'clean': 'started'}
    assert tasks2('statuses') == {'pay bill': 'completed', 'clean': 'started'}
    # sphinx-end-gettype
    sections.Section.default_gettype = 'hybrid'  # set back

    sect = sections(x=['a', 'b'])

    assert sect.sections.names == [0, 1]
    assert sect.name is sections.SectionNone
    # the string representation of sections.SectionNone is 'root'
    assert str(sect.name) == 'section'
