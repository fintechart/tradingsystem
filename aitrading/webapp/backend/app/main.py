# coding=utf-8

"""Entry point for the application."""
from . import app    # For application discovery by the 'flask' command.
from . import static
from . import services  # For import side-effects of setting up routes.
#from .entities.entity import engine
#engine.dispose()

