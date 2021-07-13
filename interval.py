from __future__ import annotations
"""                                                                                  """
"""         ██╗███╗   ██╗████████╗███████╗██████╗ ██╗   ██╗ █████╗ ██╗               """
"""         ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██║   ██║██╔══██╗██║               """
"""         ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██║   ██║███████║██║               """
"""         ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══██║██║               """
"""         ██║██║ ╚████║   ██║   ███████╗██║  ██║ ╚████╔╝ ██║  ██║███████╗          """
"""         ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝          """
"""                                                                                  """
""" Module Name: pitch                                                               """
""" Author: Luo Zhong-qi("luozhongqi@mail.com")                                      """
""" Last modified: 2021-06-08                                                        """
"""                                                                                  """
""" Description: Defined all the attributes and operations of intervals without      """
"""              modes and scales.                                                   """
"""                                                                                  """
""" Exported classes:                                                                """
"""     AbstractInterval, GenericInterval, Interval                                  """
"""                                                                                  """
""" Exported constants:                                                              """
"""     INTERVALS(dict)                                                              """

from typing import Union
from enum import Enum
import pitch
import utils

# Interval qualities constant defination
class INTERVAL_QUALITIES(Enum):
    d = -2 # diminished
    m = -1 # minor
    P = 0 # perfect
    M = 1 # major
    A = 2 # augmented

# Interval names constant defination
INTERVALS = {
    'P1': 0, # Perfect 1st, Unison
    'm2': 1, # Minor 2nd, the follows are the same
    'A1': 1, # Augmented 1st, the follows are the same
    'M2': 2, # Major 2nd, the follows are the same
    'd3': 2, # Diminshed 3rd, the follows are the same
    'm3': 3,
    'A2': 3,
    'M3': 4,
    'd4': 4,
    'P4': 5, # Perfect 4th, the follows are the same
    'A3': 5,
    'A4': 6,
    'd5': 6,
    'P5': 7,
    'd6': 7,
    'm6': 8,
    'A5': 8,
    'M6': 9,
    'd7': 9,
    'm7': 10,
    'A6': 10,
    'M7': 11,
    'P8': 12
}


class AbstractInterval:
    """
    Describes intervals without specific pitchs.

    Properties:
        name: Name of the interval.
        size: number of semitones of the interval.

    Methods:
        __init__(self, interval: Constructor of the class.
        __repr__(self): Representer of the class.
        set(self, interval): Set interval of this instance with interval name or interval size.
        invert(self): Evaluate inversion of this interval instance.

    Static Methods:
        eval(rootPitch, topPitch): Evaluate interval between root pitch and top pitch.
        eval_min(pitch1, pitch2): Evaluate minimal interval between two pitches. The position of pitches may be inverted.
    """

    __name = 'P1'

    def __init__(self, interval: Union[int, str]) -> None:
        """
        Constructor of the class.

        Arguments:
            interval[int: 0-12]: The semitone number fo the interval. Natural or diminished intervals are prior if using int as argument.
            or interval[str: member of "INTERVALS"]: The interval name. Using this as argument is recommend.

        Return:
            instance[AbstractInterval]: The interval instance according to the arguments.
        """
        self.set(interval)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return "intervalName: {}, intervalSize: {}".format(self.__name, self.size)

    def set(self, interval: Union[int, str]) -> None:
        """
        Set interval of this instance with interval name or interval size.

        Arguments:
            interval[int: 0-12]: The semitone number fo the interval. Natural or diminished intervals are prior if using int as argument.
            or interval[str: member of "INTERVALS"]: The interval name. Using this as argument is recommend.
        """
        if(interval in INTERVALS):
            self.__name = interval
        elif(isinstance(interval, int) and -1 < interval < 13):
            self.__name = utils.search_dict_by_value(INTERVALS, interval)[0] # Natural intervals are prior
        else:
            raise TypeError('"interval" must be a integer between 0 and 12 or a member in the dictionary "INTERVALS".')

    def invert(self):
        """
        Evaluate inversion of this interval instance.

        Return:
            instance[AbstractInterval]: The inversion of the original interval instance.

        Example:
            i = AbstractInterval("A4")
            i.invert()
            print(i) # Prints "d5"
        """

        return AbstractInterval(INTERVAL_QUALITIES(-INTERVAL_QUALITIES[self.__name[0]].value).name +
                                str(9 - int(self.__name[1])))

    @staticmethod
    def eval(rootPitch: pitch.GenericPitch, topPitch: pitch.GenericPitch) -> AbstractInterval:
        """
        Evaluate interval between root pitch and top pitch.

        Arguments:
            rootPitch[Pitch]: The root pitch of the interval.
            topPitch[Pitch]: The top pitch of the interval.

        Return:
            instance[Interval]: The interval constructed by the root pitch and the top pitch.

        Example:
            rp = GenericPitch("F")
            tp = GenericPitch("E")
            i = AbstractInterval.eval(rp, tp) # Prints "M7"
        """
        intervalSize = topPitch.number - rootPitch.number
        degreeSize = ord(topPitch.name) - ord(rootPitch.name)

        intervalSize = intervalSize if (intervalSize >= 0) else (12 + intervalSize) # Interval size should be a positive value.
        degreeSize = degreeSize if (degreeSize >= 0) else (degreeSize + 7) # Interval size should also be a positive value.

        intervalNames = utils.search_dict_by_value(INTERVALS, intervalSize) # Find possible interval names.
        # Find the unique interval name.
        for intervalName in intervalNames:
            if(int(intervalName[-1]) - 1 == degreeSize):
                return AbstractInterval(intervalName)

        # Enharmonic if no found
        return AbstractInterval(intervalNames[0])

    @staticmethod
    def eval_min(pitch1: pitch.GenericPitch, pitch2: pitch.GenericPitch) -> AbstractInterval:
        """
        Evaluate minimal interval between two pitches. The position of pitches may be inverted.

        Arguments:
            pitch1[Pitch]: A pitch.
            pitch2[Pitch]: Other pitch.

        Return:
            instance[Interval]: The minimal interval constructed by the pitches.

        Example:
            p1 = GenericPitch("F")
            p2 = GenericPitch("E")
            i = AbstractInterval.eval_min(p1, p2) # Prints "m2"
        """
        if (abs(pitch1.number - pitch2.number) <
            abs(pitch2.number - pitch1.number)):
            return AbstractInterval.eval(pitch1, pitch2)
        else:
            return AbstractInterval.eval(pitch2, pitch1)

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return INTERVALS[self.__name]


class GenericInterval(AbstractInterval):
    """
    Describes intervals with octaves but without specific pitchs.

    Inheritance:
        AbstractInterval

    Properties:
        name: Name of the interval.
        size: semitone number of the interval.

    Methods:
        __init__(self, interval: Constructor of the class.
        __repr__(self): Representer of the class.
        set(self, interval): Set interval of this instance with interval name or interval size.
        invert(self, interval): Evaluate inversion of this interval instance.

    Static Methods:
        eval(rootPitch, topPitch): Evaluate interval between root pitch and top pitch.
        eval_min(pitch1, pitch2): Evaluate minimal interval between two pitches. The position of pitches may be shifted.
    """
    pass #TODO(Luo Zhong-qi): Waiting for realize...


class Interval(GenericInterval):
    """
    Describes intervals with specific pitchs and octaves.

    Inheritance:
        GenericInterval

    Properties:
        name: Name of the interval.
        size: semitone number of the interval.

    Methods:
        __init__(self, interval: Constructor of the class.
        __repr__(self): Representer of the class.
        set(self, interval): Set interval of this instance with interval name or interval size.
        invert(self, interval): Evaluate inversion of this interval instance.

    Static Methods:
        eval(rootPitch, topPitch): Evaluate interval between root pitch and top pitch.
        eval_min(pitch1, pitch2): Evaluate minimal interval between two pitches. The position of pitches may be shifted.
    """
    pass #TODO(Luo Zhong-qi): Waiting for realize...