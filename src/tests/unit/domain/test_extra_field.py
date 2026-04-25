import pytest

from deps_enrichment.domain.exceptions import IllegalArgument


@pytest.mark.extra_field
@pytest.mark.parametrize(
    "name,is_valid",
    (
        ("1", True),
        ("en", True),
        ("Words with spaces", True),
        ("1234#%$(}-", True),
        ("snake_case", True),
        ("Words-with-dashes", True),
        ("Words-with-dashes and spaces", True),
        ("", False),
        ("  ", False),
        ("trailing spaces  ", False),
        ("  starting spaces", False),
        ("   multi   spaces   ", False),
    ),
)
def test_extra_field_name__checked(name, is_valid, extra_field_factory):
    if is_valid:
        assert extra_field_factory(name=name).name == name
    else:
        with pytest.raises(IllegalArgument):
            extra_field_factory(name=name)
