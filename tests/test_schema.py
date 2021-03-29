from api.db.schema import Event, Data, Place, Regularity


def test_place():
    dummy_data = {"name": "Queerreferat", "not_a_col": "not_a_col"}
    place_data = Place.drop_non_columns(dummy_data)

    assert "not_a_col" not in place_data.keys()
    place = Place(**place_data)

    extracted_data = place.to_dict()
    del extracted_data["id"]
    assert extracted_data == place_data
