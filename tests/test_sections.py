from copy import deepcopy

import pytest

from sections import Section
from sections import sections

from .test_doc_examples import test_docs_examples_details
from .test_doc_examples import test_docs_examples_usage


def get_basic_menu() -> Section:
    return sections(
        'Breakfast', 'Dinner',
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )


def func_for_property_test() -> str:
    return 'name'


def assert_menu(menu: Section) -> None:
    assert menu.names == ['Breakfast', 'Dinner']
    assert menu.sections.names == ['Breakfast', 'Dinner']
    assert menu.children.names == ['Breakfast', 'Dinner']
    assert menu.leaves.names == ['Breakfast', 'Dinner']
    assert menu.entries.names == ['Breakfast', 'Dinner']
    assert menu.mains == ['Bacon&Eggs', 'Burger']
    assert menu.sides == ['HashBrown', 'Fries']
    assert menu['Breakfast'].main == 'Bacon&Eggs'
    assert menu['Breakfast'].side == 'HashBrown'
    assert menu['Dinner'].main == 'Burger'
    assert menu['Dinner'].side == 'Fries'
    assert isinstance(menu, sections.Section)
    assert isinstance(menu['Breakfast'], sections.Section)
    assert isinstance(menu['Dinner'], sections.Section)


def test_misc1() -> None:
    # test children from dict
    menu = get_basic_menu()
    assert_menu(menu)
    menu['Dinner'] = dict(main='Burger', side='Fries')
    assert_menu(menu)
    menu['Lunch'] = dict(main='BLT', side='LunchFries')
    assert menu['Lunch'].main == 'BLT'
    assert menu['Lunch'].side == 'LunchFries'
    assert menu.mains == ['Bacon&Eggs', 'Burger', 'BLT']
    assert menu.sides == ['HashBrown', 'Fries', 'LunchFries']
    # test setting names from kwds and setting singular attr (main)
    s = sections(0, 1, x=[[0, 1], [2, 3]])
    assert s.x == [0, 1, 2, 3]
    s[0].x = [4, 5]
    assert s.x == [4, 5, 2, 3]
    menu = sections(
        'wrong name 1', 'wrong name 2',
        # test that names kwd will take priority for names over the args
        name=['Breakfast', 'Dinner'],
    )
    assert menu.names == ['Breakfast', 'Dinner']
    menu = sections(
        'wrong name 1', 'wrong name 2',
        # test that names kwd will take priority for names over the args
        names=['Breakfast', 'Dinner'],
        main=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )
    assert_menu(menu)


def test_misc2() -> None:
    # test corner case setting names to property or callable (invalid values)
    menu = sections(
        name=property(func_for_property_test),
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )
    assert func_for_property_test() == 'name'
    assert menu.names == [0, 1]
    with pytest.raises(ValueError):
        menu['Lunch'] = 0
    with pytest.raises(KeyError):
        menu['Lunch']
    with pytest.raises(AttributeError):
        menu.lunch
    # test getattr through __call__
    menu = get_basic_menu()
    assert menu('names') == ['Breakfast', 'Dinner']
    assert menu('mains') == ['Bacon&Eggs', 'Burger']
    # test uneven attrs
    menu = sections(
        'Breakfast', 'Dinner',
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown'],
    )
    assert menu.mains == ['Bacon&Eggs', 'Burger']
    assert menu.sides == 'HashBrown'
    # test full_dict
    menu = sections('Breakfast', 'Dinner', sides=['HashBrown', 'Fries'])
    assert repr(menu('sides', 'full_dict')) == repr({
        'Breakfast': 'HashBrown', 'Dinner': 'Fries'
    })


def test_cls_attrs() -> None:
    s = sections()
    s[0] = sections()
    s[0].cls.default_gettype = dict
    assert s.default_gettype == dict
    s[0] = s.cls()
    s[0].cls.default_gettype = dict
    assert s.default_gettype == dict
    s[0].default_gettype = dict
    assert s.default_gettype == dict
    s = sections()
    s[0] = sections()
    s.cls.default_gettype = dict
    assert s[0].default_gettype == dict
    sections.Section.default_gettype = dict
    s = sections([0, 1])
    assert s.cls.default_gettype == dict
    sections.Section.default_gettype = list
    s = sections([0, 1])
    s1 = sections()
    s[0].cls.default_gettype = dict
    assert s.default_gettype == dict
    assert s1.default_gettype == list
    sections.Section.default_gettype = 'hybrid'  # set back to default value


def test_misc_overrides() -> None:
    s0 = sections(x=[0, 1])
    s1 = sections(x=[0, 1])
    s2 = sections(x=0)
    assert s2.x == 0
    s3 = sections(x=[0])
    assert s3[0].name.__class__ is int
    assert s3.x == 0
    assert s0
    assert s0 != s1
    assert s0 == s0
    assert s0.x == [0, 1]
    d = {s0: 0}
    for k in d:
        assert k is s0
        assert str(k) == 'section'


def test_SectionNoneType() -> None:
    from sections import SectionNone
    assert str(SectionNone) == 'section'


def test_gettypes() -> None:
    names = [
        {'root'},
        [{'child0'}, 'leaf0', 'leaf1'],
        [{'child1'}, 'leaf2', 'leaf3'],
    ]
    attrs = dict(nodename=[{'root'},
                           [{'child0'}, 'leaf0', 'leaf1'],
                           [{'child1'}, 'leaf2', 'leaf3']])
    attrs_copy = deepcopy(attrs)
    tree = sections(*names, **attrs)
    assert tree['child0'].get_node_attr('name') == 'child0'
    assert_tree(tree)
    assert attrs_copy == attrs
    tree = sections(
        *names,
        nodenames=[{'root'},
                   [{'child0'}, 'leaf0', 'leaf1'],
                   [{'child1'}, 'leaf2', 'leaf3']]
    )
    assert_tree(tree)
    # dict
    tree = sections(
        *names,
        x=[[0, 1], [2, 3]],
        y=[0, 1]
    )
    assert tree('x', gettype=dict) == {
        'leaf0': 0, 'leaf1': 1, 'leaf2': 2, 'leaf3': 3
    }
    assert tree('y', gettype=dict) == {'child0': 0, 'child1': 1}
    assert tree('name', gettype=dict) == {'root': 'root'}
    for yvalue, yiter in zip([tree.name], tree('name', gettype=iter)):
        assert yvalue == yiter
    for value, iter_ in zip(tree.y, tree('y', gettype=iter)):
        assert value == iter_
    for value, iter_ in zip(tree.x, tree('x', gettype=iter)):
        assert value == iter_


def assert_tree(tree) -> None:
    assert tree.nodename == 'root'
    assert tree['child0'].nodename == 'child0'
    assert tree['child0'].children.nodenames == ['leaf0', 'leaf1']
    assert tree['child1'].children.nodenames == ['leaf2', 'leaf3']


def test_get_node_attr() -> None:
    sect = sections({0}, 1, 2, x=[0, 1])
    assert sect.get_node_attr('name') == 0
    assert sect.get_node_attr('names') == 0
    with pytest.raises(AttributeError):
        assert sect.get_node_attr('x')


def test_use_pluralsingular() -> None:
    s = sections(0, 1)
    s.cls.use_pluralsingular = False
    with pytest.raises(AttributeError):
        s[0].names
    sect = sections({0}, 1, 2, x=[0, 1])
    assert sect.name == 0
    assert sect.names == 0
    assert sect[1].name == 1
    assert sect[1].names == 1
    assert sect.get_node_attr('name') == 0
    assert sect.get_node_attr('names') == 0

    sections.Section.use_pluralsingular = False  # turn off for all structures
    sect = sections({0}, 1, 2)
    assert sect.name == 0
    with pytest.raises(AttributeError):
        sect.names
    assert sect[1].name == 1
    with pytest.raises(AttributeError):
        sect[1].names
    sections.Section.use_pluralsingular = True  # set back


def test_options_variations() -> None:
    Section.use_cache = False
    test_docs_examples_usage()
    test_docs_examples_details()
    Section.use_cache = True
    test_docs_examples_usage()
    test_docs_examples_details()
