#!/usr/bin/python3

from flask import Flask

app = Flask("tamagochi")

@app.route("/", methods=["GET"])
def homepage():
    return "<h1>Welcome to the new Tamagochi!<h1>";

@app.route("/auth/register", methods=["POST"])
def register():
    return "";

@app.route("/auth/login", methods=["POST"])
def login():
    return "";


