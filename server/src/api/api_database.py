"""
    Simple config file to share DB connection in type files
"""
from database.controller import Controller
db = Controller(host="redis")
