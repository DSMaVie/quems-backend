from api.db.schema import Event, Data, Place, Regularity
import pytest


@pytest.mark.parametrize(
    "schema_cls,dummy_data",
    [(Place, {"name": "testname"}), (Regularity, {"outdated": True})],
)  # , need to fill with data)
def test_schema(schema_cls, dummy_data):
    dummy_data |= {"not_a_col": None}
    cleaned_data = schema_cls.drop_non_columns(dummy_data)
    assert "not_a_col" not in cleaned_data.keys()

    schema_obj = schema_cls(**cleaned_data)
    extracted_data = schema_obj.to_dict()

    assert extracted_data.items() >= cleaned_data.items()
