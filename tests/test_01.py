from hatch_pre_index import hatch_pre_index


def test_1():
    obj = hatch_pre_index()

    arg1 = "blabla"
    assert obj.for_test_only(arg1) == arg1

