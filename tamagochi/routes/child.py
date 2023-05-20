#!/bin/python 

from flask import Blueprint

child = Blueprint("parent", __name__, url_prefix="/child")

@child.route("/parent", methods=["GET"])
def child():
    return "hello child!"
