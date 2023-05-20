#!/bin/python3

def checkFields(data_obj, *fields):
    for value in fields:
        if data_obj.get(value) is None:
            return False

    return True