#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
from abc import ABC, abstractmethod


class Figure(ABC):

    @abstractmethod
    def build(self):
        pass
