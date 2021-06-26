import pytest

import sections


def test_indepth_usage() -> None:
    """
    This is especially for making sure the cache feature works correctly as the
    structure is modified.
    """
    s = sections(
        y=[['0', '1'], ['2', '3']],
        z=[['0', '1'], ['2', '3']],
    )
    assert_leaf_var(s, 'y')
    assert_leaf_var(s, 'z')
    s.x = [['0', '1'], ['2', '3']]
    assert_no_mod(s, 'x')
    s[0].x = [0, 1]
    assert_L01_mod(s, 'x')
    s[1].x = [2, 3]
    assert_L0123_mod(s, 'x')
    s[1].x = ['2', '3']
    assert_L01_mod(s, 'x')
    s[0].x = ['0', '1']
    assert_no_mod(s, 'x')


def assert_leaf_var(s, var):
    """Modify node attrs then set them back, check correctness at each step."""
    # Start modifying node attributes
    setattr(s[0][0], var, 0)
    assert_L0_mod(s, var)
    setattr(s[0], var, 10)
    assert_c0_L0_mod(s, var)
    setattr(s[1][1], var, 3)
    assert_c0_L03_mod(s, var)
    setattr(s[1], var, 20)
    assert_c01_L03_mod(s, var)

    # Start setting the structure back to its original state
    delattr(s[1], var)
    assert_c0_L03_mod(s, var)
    setattr(s[1][1], var, '3')
    assert_c0_L0_mod(s, var)
    delattr(s[0], var)
    assert_L0_mod(s, var)
    setattr(s[0][0], var, '0')
    assert_no_mod(s, var)


def assert_no_mod(s, var):
    """Assert original structure state."""
    assert s(var) == ['0', '1', '2', '3']
    assert s.all_leaves(var) == ['0', '1', '2', '3']
    assert s.children(var) == ['0', '1', '2', '3']


def assert_L0_mod(s, var):
    """Assert after only leaf0 has a modification."""
    assert s(var) == [0, '1', '2', '3']
    assert s.children(var) == [0, '1', '2', '3']
    assert s.all_leaves(var) == [0, '1', '2', '3']
    assert s[0](var) == [0, '1']
    assert s[0].children(var) == [0, '1']
    assert s[0].all_leaves(var) == [0, '1']
    assert s[0][0](var) == 0
    with pytest.raises(AttributeError):
        s[0][0].children(var)
    # TODO: this should raise AttributeError:
    # with pytest.raises(AttributeError):
        # s[0][0].leaves(var)


def assert_L01_mod(s, var):
    """Assert after only leaf0 has a modification."""
    assert s(var) == [0, 1, '2', '3']
    assert s.children(var) == [0, 1, '2', '3']
    assert s.all_leaves(var) == [0, 1, '2', '3']
    assert s[0](var) == [0, 1]
    assert s[0].children(var) == [0, 1]
    assert s[0].all_leaves(var) == [0, 1]
    assert s[0][0](var) == 0
    with pytest.raises(AttributeError):
        s[0][0].children(var)
    # TODO: this should raise AttributeError:
    # with pytest.raises(AttributeError):
        # s[0][0].all_leaves(var)


def assert_L0123_mod(s, var):
    """Assert after only leaf0 has a modification."""
    assert s(var) == [0, 1, 2, 3]
    assert s.children(var) == [0, 1, 2, 3]
    assert s.all_leaves(var) == [0, 1, 2, 3]
    assert s[0](var) == [0, 1]
    assert s[0].children(var) == [0, 1]
    assert s[0].all_leaves(var) == [0, 1]
    assert s[0][0](var) == 0
    assert s[1](var) == [2, 3]
    assert s[1].children(var) == [2, 3]
    assert s[1].all_leaves(var) == [2, 3]
    assert s[1][1](var) == 3
    with pytest.raises(AttributeError):
        s[0][0].children(var)
    # TODO: this should raise AttributeError:
    # with pytest.raises(AttributeError):
        # s[0][0].all_leaves(var)
    with pytest.raises(AttributeError):
        s[1][1].children(var)
    # TODO: this should raise AttributeError:
    # with pytest.raises(AttributeError):
        # s[1][1].all_leaves(var)


def assert_c0_L0_mod(s, var):
    """Assert after child0, leaf0 have a modification."""
    assert s(var) == [10, '2', '3']
    assert s.children(var) == [10, '2', '3']
    assert s.all_leaves(var) == [0, '1', '2', '3']
    assert s[0](var) == 10
    assert s[0].all_leaves(var) == [0, '1']
    assert s[0][0](var) == 0


def assert_c0_L03_mod(s, var):
    """Assert after child0, leaf0, leaf3 have a modification."""
    assert s(var) == [10, '2', 3]
    assert s.children(var) == [10, '2', 3]
    assert s.all_leaves(var) == [0, '1', '2', 3]
    assert s[1](var) == ['2', 3]
    assert s[1].children(var) == ['2', 3]
    assert s[1].all_leaves(var) == ['2', 3]
    assert s[1][1](var) == 3
    with pytest.raises(AttributeError):
        s[1][1].children(var)
    # TODO: this should raise AttributeError:
    # with pytest.raises(AttributeError):
        # s[1][1].all_leaves(var)


def assert_c01_L03_mod(s, var):
    """Assert after child0, child1, leaf0, leaf3 have a modification."""
    assert s(var) == [10, 20]
    assert s.children(var) == [10, 20]
    assert s.all_leaves(var) == [0, '1', '2', 3]
    assert s[1](var) == 20
    assert s[1].all_leaves(var) == ['2', 3]
    assert s[1][1](var) == 3
