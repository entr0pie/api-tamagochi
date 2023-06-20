
def verifyFields(data: dict, all_fields: tuple) -> bool:
    """Verify if the data sent match with all the fields needed."""

    data_keys = data.keys()

    for key in fields:
        if key not in data_keys:
            return False 

    return True
