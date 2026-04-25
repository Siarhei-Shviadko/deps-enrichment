from deps_enrichment.api import SerializedExtraField


def test_from_model(extra_field):
    serialized_field = SerializedExtraField.from_model(extra_field)

    assert serialized_field.code == extra_field.code()
    assert serialized_field.name == extra_field.name
    assert serialized_field.type == extra_field.type
    assert serialized_field.auto_filled == extra_field.auto_filled
    assert serialized_field.display_order == extra_field.display_order

    raw_field = serialized_field.dict(by_alias=True)

    assert raw_field["code"] == extra_field.code()
    assert raw_field["name"] == extra_field.name
    assert raw_field["type"] == extra_field.type
    assert raw_field["autoFilled"] == extra_field.auto_filled
    assert raw_field["order"] == extra_field.display_order
