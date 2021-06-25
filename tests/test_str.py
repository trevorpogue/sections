import sections


def test_str_breadthfirst() -> None:
    """Test the printing string representation functions."""
    library = sections(
        {"My Bookshelf"},
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Mathematics', 'Physics for Engineers'],
        topics=[{'All my books'},
                [{'Imaginary things'}, 'Hobbits', 'Wizards'],
                [{'School'}, 'Numbers', 'Forces']],
    )
    node_str = library.node_str()
    deep_str_breadthfirst = library.deep_str()
    expected_node_str = (
        ""
        + "'My Bookshelf' = <root, parent>"
        + "\n    parent = None"
        + "\n    children = ['Fantasy', 'Academic']"
        + "\n    topics = 'All my books'\n"
    )

    expected_deep_str_breadthfirst = (
        ""
        + "#######################################"
        + "########################################"
        + "\n<class 'Section'> structure"
        + "\n"
        + "\n'My Bookshelf' = <root, parent>"
        + "\n    parent = None"
        + "\n    children = ['Fantasy', 'Academic']"
        + "\n    topics = 'All my books'"
        + "\n"
        + "\n'Fantasy' = <child, parent>"
        + "\n    parent = 'My Bookshelf'"
        + "\n    children = ['LOTR', 'Harry Potter']"
        + "\n    topics = 'Imaginary things'"
        + "\n"
        + "\n'Academic' = <child, parent>"
        + "\n    parent = 'My Bookshelf'"
        + "\n    children = ['Advanced Mathematics', 'Physics for Engineers']"
        + "\n    topics = 'School'"
        + "\n"
        + "\n'LOTR' = <child, leaf>"
        + "\n    parent = 'Fantasy'"
        + "\n    topics = 'Hobbits'"
        + "\n"
        + "\n'Harry Potter' = <child, leaf>"
        + "\n    parent = 'Fantasy'"
        + "\n    topics = 'Wizards'"
        + "\n"
        + "\n'Advanced Mathematics' = <child, leaf>"
        + "\n    parent = 'Academic'"
        + "\n    topics = 'Numbers'"
        + "\n"
        + "\n'Physics for Engineers' = <child, leaf>"
        + "\n    parent = 'Academic'"
        + "\n    topics = 'Forces'"
        + "\n######################################"
        + "#########################################\n"
    )
    assert str(library) == 'My Bookshelf'
    assert node_str == expected_node_str
    assert deep_str_breadthfirst == expected_deep_str_breadthfirst


def test_str_depthfirst() -> None:
    library = sections(
        {"My Bookshelf"},
        [{'Fantasy'}, 'LOTR', 'Harry Potter'],
        [{'Academic'}, 'Advanced Mathematics', 'Physics for Engineers'],
        topics=[{'All my books'},
                [{'Imaginary things'}, 'Hobbits', 'Wizards'],
                [{'School'}, 'Numbers', 'Forces']],
    )
    deep_str_depthfirst = library.deep_str(breadthfirst=False)
    expected_deep_str_depthfirst = (
        ""
        + "#######################################"
        + "########################################"
        + "\n<class 'Section'> structure"
        + "\n"
        + "\n'My Bookshelf' = <root, parent>"
        + "\n    parent = None"
        + "\n    children = ['Fantasy', 'Academic']"
        + "\n    topics = 'All my books'"
        + "\n"
        + "\n'Fantasy' = <child, parent>"
        + "\n    parent = 'My Bookshelf'"
        + "\n    children = ['LOTR', 'Harry Potter']"
        + "\n    topics = 'Imaginary things'"
        + "\n"
        + "\n'LOTR' = <child, leaf>"
        + "\n    parent = 'Fantasy'"
        + "\n    topics = 'Hobbits'"
        + "\n"
        + "\n'Harry Potter' = <child, leaf>"
        + "\n    parent = 'Fantasy'"
        + "\n    topics = 'Wizards'"
        + "\n"
        + "\n'Academic' = <child, parent>"
        + "\n    parent = 'My Bookshelf'"
        + "\n    children = ['Advanced Mathematics', 'Physics for Engineers']"
        + "\n    topics = 'School'"
        + "\n"
        + "\n'Advanced Mathematics' = <child, leaf>"
        + "\n    parent = 'Academic'"
        + "\n    topics = 'Numbers'"
        + "\n"
        + "\n'Physics for Engineers' = <child, leaf>"
        + "\n    parent = 'Academic'"
        + "\n    topics = 'Forces'"
        + "\n######################################"
        + "#########################################\n"
    )
    assert deep_str_depthfirst == expected_deep_str_depthfirst
