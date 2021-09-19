#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


@dataclass()
class Line:
    start: Point
    end: Point


def points2line(points: list[tuple[float, float], tuple[float, float]]):
    return Line(Point(points[0][0], points[0][1]), Point(points[1][0], points[1][1]))


def line2points(line: Line):
    return [(line.start.x, line.start.y), (line.end.x, line.end.y)]

