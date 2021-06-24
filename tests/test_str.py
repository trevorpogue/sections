import sections


def test_str_breadthfirst() -> None:
    """Test the printing string representation functions."""
    s = sections({'root'}, [{'c0'}, 'L0', 'L1'], [{'c1'}, 'L2', 'L3'])
    node_str = s.node_str()
    deep_str_breadthfirst = s.deep_str()
    expected_node_str = (
        "<class 'sections.Sections.UniqueSection.<locals>.Section'>:"
        + " root, parent\n"
        + "children            : ['c0', 'c1']\n"
        + "name                : 'root'\n"
        + "parent              : None\n"
    )

    expected_deep_str_breadthfirst = (
        ""
        + "#######################################"
        + "########################################"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: root, parent"
        + "\nchildren            : ['c0', 'c1']"
        + "\nname                : 'root'"
        + "\nparent              : None"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, parent"
        + "\nchildren            : ['L0', 'L1']"
        + "\nname                : 'c0'"
        + "\nparent              : 'root'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, parent"
        + "\nchildren            : ['L2', 'L3']"
        + "\nname                : 'c1'"
        + "\nparent              : 'root'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L0'"
        + "\nparent              : 'c0'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L1'"
        + "\nparent              : 'c0'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L2'"
        + "\nparent              : 'c1'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L3'"
        + "\nparent              : 'c1'"
        + "\n#######################################"
        + "########################################\n"
    )
    assert (str(s) == 'root')
    assert (node_str == expected_node_str)
    assert (deep_str_breadthfirst == expected_deep_str_breadthfirst)


def test_str_depthfirst() -> None:
    s = sections({'root'}, [{'c0'}, 'L0', 'L1'], [{'c1'}, 'L2', 'L3'])
    deep_str_depthfirst = s.deep_str(breadthfirst=False)
    expected_deep_str_depthfirst = (
        ""
        + "#######################################"
        + "########################################"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: root, parent"
        + "\nchildren            : ['c0', 'c1']"
        + "\nname                : 'root'"
        + "\nparent              : None"
        + "\n<class 'sections.Sections.UniqueSection."
        + "<locals>.Section'>: child, parent"
        + "\nchildren            : ['L0', 'L1']"
        + "\nname                : 'c0'"
        + "\nparent              : 'root'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L0'"
        + "\nparent              : 'c0'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L1'"
        + "\nparent              : 'c0'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, parent"
        + "\nchildren            : ['L2', 'L3']"
        + "\nname                : 'c1'"
        + "\nparent              : 'root'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L2'"
        + "\nparent              : 'c1'"
        + "\n<class 'sections.Sections.UniqueSection"
        + ".<locals>.Section'>: child, leaf"
        + "\nname                : 'L3'"
        + "\nparent              : 'c1'"
        + "\n######################################"
        + "#########################################\n"
    )
    assert (str(s) == 'root')
    assert (deep_str_depthfirst == expected_deep_str_depthfirst)
