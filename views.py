from __future__ import annotations
from typing import Callable
from abc import ABC, abstractmethod


class Context:
    -state = None
    def __init__(self, state:State) -> None:

        self.go(state)

    def go(self, state:State):
        """
        todo:add log here to find transition of states
        """
        self._state = state
        self._state.context = self


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handler(self):
        pass


class Reservation(State):
    def handler(self):
        """
        do some logic here :->
        """
        self.context.go(self)
