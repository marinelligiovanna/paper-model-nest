import enum
from pynest.elements.rect import Rect
import typing as tp
from functools import cmp_to_key

class SortMethod:
    ASCA = "asca"
    DESCA = "desca"
    ASCSS = "ascss"
    DESCSS = "descss"
    ASCLS = "ascls"
    DESCLS = "descls"
    ASCPERIM = "ascperim"
    DESCPERIM = "descperim"
    ASCDIFF = "ascdiff"
    DESCDIFF = "descdiff"
    ASCRATIO = "ascratio"
    DESCRATIO = "descratio"

def area_comparator(r1: Rect, r2:Rect):
    return r1.area() - r2.area()

def shorterside_comparator(r1:Rect, r2:Rect):
    if r1.width == r2.width:
        return r1.height - r2.height
    return r1.width - r2.width

def longerside_comparator(r1:Rect, r2:Rect):
    if r1.height == r2.height:
        return r1.width - r2.width
    return r1.height - r2.height

def perimeter_comparator(r1:Rect, r2:Rect):
    return r1.width + r1.height < r2.width + r2.height

def difside_comparator(r1:Rect, r2:Rect):
    return abs(r1.width - r1.height) - abs(r2.width - r2.height)

def ratio_comparator(r1:Rect, r2:Rect):
    return r1.width/r1.height - r2.width/r2.height

area_key = cmp_to_key(area_comparator)
shorterside_key = cmp_to_key(shorterside_comparator)
longerside_key = cmp_to_key(longerside_comparator)
perimeter_key = cmp_to_key(perimeter_comparator)
difside_key = cmp_to_key(difside_comparator)
ratio_key = cmp_to_key(ratio_comparator)

def sort_rects(rects: tp.List[Rect], by:str=None):
    # Area
    if by == SortMethod.ASCA:
        return sorted(rects, key=area_key)
    elif by == SortMethod.DESCA:
        return sorted(rects, key=area_key, reverse=True)

    # Shorter side
    elif by == SortMethod.ASCSS:
        return sorted(rects, key=shorterside_key)
    elif by == SortMethod.DESCSS:
        return sorted(rects, key=shorterside_key, reverse=True)

    # Longer side
    elif by == SortMethod.ASCLS:
        return sorted(rects, key=longerside_key)
    elif by == SortMethod.DESCLS:
        return sorted(rects, key=longerside_key, reverse=True)

    # Perimeter
    elif by == SortMethod.ASCPERIM:
        return sorted(rects, key=perimeter_key)
    elif by == SortMethod.DESCPERIM:
        return sorted(rects, key=perimeter_key, reverse=True)

    # Sides diff
    elif by == SortMethod.ASCDIFF:
        return sorted(rects, key=difside_key)
    elif by == SortMethod.DESCDIFF:
        return sorted(rects, key=difside_key, reverse=True)

    # Ratio
    elif by == SortMethod.ASCRATIO:
        return sorted(rects, key=ratio_key)
    elif by == SortMethod.DESCRATIO:
        return sorted(rects, key=ratio_key, reverse=True)

    return rects