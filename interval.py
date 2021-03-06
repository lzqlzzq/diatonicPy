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
""" Last modified: 2021-07-20                                                        """
"""                                                                                  """
""" Description: Defined all the attributes and operations of intervals without      """
"""              modes and scales.                                                   """
"""                                                                                  """
""" Exported classes:                                                                """
"""     AbstractInterval, Interval                                                   """
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
    Describes intervals without specific pitchs with octaves.

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

    __quality = "P"
    __degree = 1

    def __init__(self, interval: Union[int, str]) -> None:
        """
        Constructor of the class.

        Arguments:
            interval[int: 0-]: The semitone number fo the interval. Natural or diminished intervals are prior if using int as argument.
            or interval[str: member of "INTERVALS"]: The interval name. Format is as the INTERVALS dict. Using this as argument is recommend.

        Return:
            instance[AbstractInterval]: The interval instance according to the arguments.
        """
        self.set(interval)

    def __str__(self):
        return "{}{}".format(self.__quality, self.__degree)

    def __repr__(self):
        return "intervalName: {}, intervalSize: {}".format(str(self), self.size)

    def set(self, interval: Union[int, str]) -> None:
        """
        Set interval of this instance with interval name or interval size.

        Arguments:
            interval[int: 0-88]: The semitone number of the interval. Natural or diminished intervals are prior if using int as argument.
            or interval[str]: The interval name. Format is as the dictionary "INTERVALS". Using this as argument is recommend.
        """
        if(isinstance(interval, str)):
            interval = AbstractInterval.res_name(interval)
            self.__quality = interval[0]
            self.__degree = interval[1]
        elif(isinstance(interval, int) and 0 < interval < 88):
            singleIntervalName = utils.search_dict_by_value(INTERVALS, interval % 12)[0] # Natural intervals are prior
            self.__quality = singleIntervalName[0]
            self.__degree = interval // 12 * 7 + int(singleIntervalName[1])
        else:
            raise TypeError('"interval" must be a integer between 0 and 88 or as format of members in the dictionary "INTERVALS".')

    def invert(self):
        """
        Evaluate inversion of this interval instance.

        Return:
            instance[AbstractInterval]: The inversion of the original interval instance.

        Example:
            i = AbstractInterval("A4")
            print(i.invert()) # Prints "d5"
        """

        return AbstractInterval(INTERVAL_QUALITIES(-INTERVAL_QUALITIES[self.quality].value).name +
                                str(9 - int(self.singleDegree) + self.octave * 7))

    @staticmethod
    def res_name(intervalName: str) -> tuple:
        if(intervalName[0] in INTERVAL_QUALITIES.__members__):
            quality = intervalName[0]
        else:
            raise ValueError("Interval quality must be M, m, P, A, d(major, minor, perfect, augmented, diminished).")
        if(1 <= int(intervalName[1:]) <= 52):
            degree = int(intervalName[1:])
        else:
            raise ValueError("Interval degree must between 1 and 52.")
        return (quality, degree)

    @staticmethod
    def eval(rootPitch: Union[pitch.GenericPitch, pitch.Pitch], topPitch: Union[pitch.GenericPitch, pitch.Pitch]) -> AbstractInterval:
        """
        Evaluate interval between root pitch and top pitch.

        Arguments:
            rootPitch[GenericPitch or Pitch]: The root pitch of the interval.
            topPitch[GenericPitch or Pitch]: The top pitch of the interval.
            P. S.: The type of two arguments must be identical.

        Return:
            instance[AbstractInterval]: The interval constructed by the root pitch and the top pitch.

        Example:
            rp = GenericPitch("F")
            tp = GenericPitch("E")
            i = AbstractInterval.eval(rp, tp) # Prints "M7"
        """
        intervalSize = topPitch.number - rootPitch.number
        degreeSize = topPitch.scaleDegree - rootPitch.scaleDegree

        intervalSize = intervalSize if (intervalSize >= 0) else (intervalSize + 12) # Interval size should be a positive value.
        degreeSize = degreeSize + 1 if (degreeSize >= 0) else (degreeSize + 8)
        singleDegreeSize = utils.constrain_by_cycle(degreeSize, 1, 7) # Interval size should also be a positive value.
        singleIntervalSize = intervalSize % 12

        singleIntervalNames = utils.search_dict_by_value(INTERVALS, singleIntervalSize) # Find possible interval names.
        # Find the unique interval name.
        for singleIntervalName in singleIntervalNames:
            if(int(singleIntervalName[-1]) == singleDegreeSize):
                return AbstractInterval("{}{}".format(singleIntervalName[0], degreeSize))

        # Enharmonic if no found
        return AbstractInterval(singleIntervalNames[0]) # TODO(Luo Zhong-qi): Support Pitch class.

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
    def quality(self):
        return self.__quality

    @property
    def degree(self):
        return self.__degree

    @property
    def octave(self):
        return (self.degree - 1) // 7

    @property
    def singleName(self):
        return "{}{}".format(self.quality, utils.constrain_by_cycle(self.degree, 1, 7))

    @property
    def singleSize(self):
        return INTERVALS[self.singleName]

    @property
    def singleDegree(self):
        return self.degree % 7

    @property
    def size(self):
        return INTERVALS[self.singleName] + self.octave * 12


class Interval(AbstractInterval):
    """
    Describes intervals with specific pitchs and octaves.

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