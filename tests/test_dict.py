import pytest

from sections import Section
from sections import sections


def get_basic_menu() -> Section:
    return sections(
        'Breakfast', 'Dinner',
        mains=['Bacon&Eggs', 'Burger'],
        sides=['HashBrown', 'Fries'],
    )


def test_iter_methods() -> None:
    menu = get_basic_menu()
    for i, name in enumerate(menu.keys()):
        assert menu.names[i] == name
    for child1, child2 in zip(menu.children, menu.values()):
        assert child1 is child2
    for name, child in menu.items():
        assert child is menu[name]
    # test Sections.__iter__
    menu = get_basic_menu()
    names = menu.names
    for section, name in zip(menu, names):
        assert section.name == name


def test_not_implemented() -> None:
    menu = get_basic_menu()
    with pytest.raises(NotImplementedError):
        menu.clear()
    with pytest.raises(NotImplementedError):
        menu.copy()
    with pytest.raises(NotImplementedError):
        menu.setdefault(1, 1)
    with pytest.raises(NotImplementedError):
        menu.fromkeys(1, x=1)
    with pytest.raises(NotImplementedError):
        menu.get(1, x=1)
    with pytest.raises(NotImplementedError):
        menu.update(1, x=1)


def test_pop_methods() -> None:
    s0 = sections(x=[0, 1])
    s0.pop(0)
    assert s0.x == 1
    s0 = sections(x=[0, 1])
    s0.popitem()
    assert s0.x == 0
