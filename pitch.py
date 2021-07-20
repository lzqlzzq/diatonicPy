from __future__ import annotations
"""                                                                                  """
"""                  ██████╗ ██╗████████╗ ██████╗██╗  ██╗                            """
"""                  ██╔══██╗██║╚══██╔══╝██╔════╝██║  ██║                            """
"""                  ██████╔╝██║   ██║   ██║     ███████║                            """
"""                  ██╔═══╝ ██║   ██║   ██║     ██╔══██║                            """
"""                  ██║     ██║   ██║   ╚██████╗██║  ██║                            """
"""                  ╚═╝     ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝                            """
"""                                                                                  """
""" Module Name: pitch                                                               """
""" Author: Luo Zhong-qi("luozhongqi@mail.com")                                      """
""" Last modified: 2021-07-20                                                        """
"""                                                                                  """
""" Description: Defined all the attributes and operations of pitches without modes  """
"""              and scales.                                                         """
"""                                                                                  """
""" Exported classes:                                                                """
"""     NATURAL_PITCHES(Enum), ACCIDENTALS(Enum), GenericPitch, Pitch                """
"""                                                                                  """
""" Exported Constants:                                                              """
"""     PITCHES(dict)                                                                """

from enum import Enum
from typing import Union, List
import utils
import interval

# Pitch names constant defination
class NATURAL_PITCHES(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11


# Natural scale
class NATURAL_SCALE(Enum):
    C = 1
    D = 2
    E = 3
    F = 4
    G = 5
    A = 6
    B = 7


# Accidental names constant defination
class ACCIDENTALS(Enum):
    df = -2 # Double Flat
    f = -1 # Flat
    n = 0 # Natural
    s = 1 # Sharp
    ds = 2 # Double Sharp


# Pitch names constant defination
PITCHES = {
    'C': 0,
    'Bs': 0, # B Sharp, "s" for sharp, the follows are the same
    'Ddf': 0, # D Double Flat, "ds" for double flat, the follows are the same
    'Cs': 1,
    'Df': 1, # D Flat, "f" for flat, the follows are the same
    'D': 2,
    'Cds': 2,
    'Edf': 2,
    'Ds': 3,
    'Ef': 3,
    'E': 4,
    'Dds': 4,
    'Ff': 4,
    'F': 5,
    'Es': 5,
    'Gdf': 5,
    'Fs': 6,
    'Gf': 6,
    'G': 7,
    'Fds': 7,
    'Adf': 7,
    'Gs': 8,
    'Af': 8,
    'A': 9,
    'Gds': 9,
    'Bds': 9,
    'As': 10,
    'Bf': 10,
    'B': 11,
    'Ads': 11,
    'Cf': 11
}


class GenericPitch:
    """
    Describes pitches without octave.

    Properties:
        name: The name of the pitch without accidental. Using "str(GenericPitch)" to include accidental.
        accidental: The accidental of the pitch, defined by Enum "ACCIDENTALS".
        number: The number of the pitch.

    Methods:
        __init__(self, pitch): Constructor of the class.
        __repr__(self): Representer of the class.
        set_pitch(self, pitch): Set pitch of this instance with pitch name or pitch number.
        set(self, pitch): Set pitch of this instance with pitch name or pitch number.
        shift(self, interval, direction): Shift this pitch with "GenericPitch" instance and interval, and direction.

    Oprations:
        add(GenericPitch + AbstractInterval): Raise the pitch with an interval.
            e. g. "C + M3 = E" //Pseudo code, not Python
        sub(GenericPitch - AbstractInterval): Lower the pitch with an interval.
            e. g. "C - M3 = Ab"

    Static Methods:
        res_name(pitchName): Resolve the pitch name with accidental to a tuple and check the format.
            e. g. ["A", "s"] for "As".
        num_by_name(pitchName): Search pitch number by pitch name.
            e. g. 10 for As.
        names_by_num(num): Search pitch names by pitch number.
            e. g. "As", "Bf" for 10.
        name_by_num(num): Search pitch name by pitch number, natural and flat are prior.
            e. g. "Bf" for 10.
    """

    __name = 'C'
    __accidental = 'n'

    def __init__(self, pitch: Union[int, str]) -> None:
        self.set(pitch)

    def __str__(self):
        return '{}{}'.format(self.__name, '' if self.__accidental == ACCIDENTALS.n.name else self.__accidental)

    def __repr__(self):
        return "GenericPitch:\n    name: {},\n    number: {}".format(str(self), self.number)

    def set_pitch(self, pitch: Union[int, str]) -> None:
        """
        Set pitch of this instance with pitch name or pitch number.

        Arguments:
            pitch[int: 0-11]: The pitch number, "0-12" corresponding to pitch name "C-B". Natural and flat pitches are prior.
            or pitch[str: pitch name, e. g. "C, Cs, Cf"]: The pitch name, using this kind of argument is recommonded.
        """
        if(isinstance(pitch, str)):
            pitchName = GenericPitch.res_name(pitch)
            self.__name = pitchName[0]
            self.__accidental = pitchName[1]
        elif(isinstance(pitch, int)):
            pitchName = GenericPitch.res_name(GenericPitch.name_by_num(pitch))
            self.__name = pitchName[0]
            self.__accidental = pitchName[1]

    def set(self, pitch: Union[int, str]) -> None:
        """
        Set this instance with pitch name or pitch number.

        Arguments:
            pitch[int: 0-11]: The pitch number, "0-12" corresponding to pitch name "C-B". Natural and flat pitches are prior.
            or pitch[str: as format of dictionary "PITCHES"]: The pitch name, using this kind of argument is recommonded.
        """
        self.set_pitch(pitch)

    def shift(self, interval: interval.AbstractInterval, direction: int) -> GenericPitch:
        """
        Shift this pitch with interval and direction.

        Arguments:
            interval[AbstractInterval instance]: The interval to shift.
            direction[int: -1 or 1]: The direction to shift, -1 indicates to lower the pitch while 1 indicates to raise the pitch.

        Example:
            i = AbstractInterval('A4') # Augumented 4th
            p = GenericPitch('A')
            ps = p.shift_pitch(i, 1)
            print(str(ps)) # Prints "Ds"
        """
        assert (direction == -1 or direction ==1), 'Direction must be -1 or 1.'

        # calculate pitch number
        pitchNumber = self.number + direction * interval.singleSize
        pitchNumber = utils.constrain_by_cycle(pitchNumber, 0, 12)

        # find possible pitch name
        shiftedPitchName = ord(self.__name) + direction * (int(interval.singleName[1]) - 1)
        shiftedPitchName = chr(utils.constrain_by_cycle(shiftedPitchName, 65, 8)) # ASCII 65-73 = A-G

        pitchNames = GenericPitch.names_by_num(pitchNumber)
        for pitchName in pitchNames:
            if(shiftedPitchName == pitchName[0]):
                return GenericPitch(pitchName)

        # enharmonic if no found
        return GenericPitch(pitchNames[int(1 - direction / 2)])

    @staticmethod
    def res_name(pitchName: str) -> tuple:
        """
        Resolve the pitch name with accidental to a tuple and check the format.

        Argument:
            pitchName[str]: The pitch name with accidental e. g. "As" "C" "Fds".

        Return:
            resolvedName[tuple]: Resolved name e. g. ["A", "s"].
        """
        # check argument
        if(pitchName[0] in NATURAL_PITCHES.__members__):
            name = pitchName[0]
        else:
            raise ValueError('Pitch name must be one of "C", "D", "E", "F", "G", "A", "B".')

        if(len(pitchName) == 1):
            accidental = ACCIDENTALS.n.name
        elif(pitchName[1:] in ACCIDENTALS.__members__):
            accidental = pitchName[1:]
        else:
            raise ValueError('The accidental of pitch name must be one of "s", "f", "ds", "df", or "n".')

        return (name, accidental)

    @staticmethod
    def num_by_name(pitchName: str) -> int:
        """
        Search pitch number by pitch name.

        Argument:
            name[str]: The pitch name with accidental e. g. "As" "C" "Fds".

        Return:
            pitchNum[int]: The pitch number e. g. 10 for As.
        """
        pitchName = GenericPitch.res_name(pitchName)
        return (NATURAL_PITCHES[pitchName[0]].value + ACCIDENTALS[pitchName[1]].value) % 12

    @staticmethod
    def names_by_num(num: int) -> List:
        """
        Search pitch names by pitch number.

        Argument:
            num[int: 0-11]: The pitch number, from 0 to 11.

        Return:
            names[List:[int]]: The pitch names e. g. "As", "Bf" for 10.
        """
        # check argument
        if(not(0 <= num < 12)):
            raise ValueError('Pitch number must be an integer between 0 and 11.')

        names = []
        try:
            names.apppend(NATURAL_PITCHES(num).name, ACCIDENTALS.n.name)
        except:
            names = utils.search_dict_by_value(PITCHES, num)

        return names

    @staticmethod
    def name_by_num(num: int) -> str:
        """
        Search pitch name by pitch number, natural and flat are prior.

        Argument:
            num[int: 0-11]: The pitch number, from 0 to 11.

        Return:
            name[int]: The pitch names e. g. "Bf" for 10.
        """
        if(not(0 <= num < 12)):
            raise ValueError('Pitch number must be an integer between 0 and 11.')

        try:
            return "{}".format(NATURAL_PITCHES(num).name)
        except:
            return "{}f".format(NATURAL_PITCHES(num + 1).name)


    def __add__(self, interval: AbstractInterval) -> GenericPitch:
        """
        Raise this pitch with interval.

        Arguments:
            interval[AbstractInterval instance]: The interval to raise.

        Example:
            p = GenericPitch('A')
            i = AbstractInterval('A4')
            pa = p + i # Here comes the opration
            print(pa.name) # Print "Ds"
        """
        return self.shift(interval, 1)

    def __sub__(self, interval: AbstractInterval) -> GenericPitch:
        """
        Lower this pitch with interval.

        Example:
            p = GenericPitch('A')
            i = AbstractInterval('A4')
            pa = p - i # Here comes the opration
            print(pa.name) # Print "Eb"
        """
        return self.shift(interval, -1)

    @property
    def name(self):
        return self.__name

    @property
    def accidental(self):
        return self.__accidental
    
    @property
    def number(self):
        return (NATURAL_PITCHES[self.__name].value + ACCIDENTALS[self.__accidental].value) % 12

    @property
    def scaleDegree(self):
        return NATURAL_SCALE[self.__name].value
    

class Pitch(GenericPitch):
    """
    Describes pitches with octave.

    Properties:
        name: The name of the pitch without accidental. Using "str(Pitch)" to include accidental.
        accidental: The accidental of the pitch, defined by Enum "ACCIDENTALS".
        number: The generic number of the pitch.
        octave: The octave number of the pitch in Science Pitch Notation.
        MIDInumber: The MIDI number of the pitch.

    Methods:
        __init__(self, pitch): Constructor of the class.
        __repr__(self): Representer of the class.
        set_pitch(self, pitch): Set pitch of this instance with pitch name or pitch number.
        set(self, pitch): Set pitch of this instance with pitch name or pitch number.
        shift(self, interval, direction): Shift this pitch with "GenericPitch" instance and interval, and direction.

    Oprations:
        add[GenericPitch + AbstractInterval]: Raise the pitch with an interval.
            e. g. "C4 + M3 = E4" //Pseudo code, not Python
        sub[GenericPitch - AbstractInterval]: Lower the pitch with an interval.
            e. g. "C4 - M3 = Ab3"

    Static Methods:
        res_name(pitchName): Resolve the pitch name with accidental to a tuple and check the format.
            e. g. ["A", "s", 4] for "As4".
        MIDI_num_by_name(pitchName): Search pitch number by pitch name.
            e. g. 60 for C4.
        names_by_MIDI_num(num): Search pitch names by pitch number.
            e. g. "Bs3", "C4" for 60.
        name_by_MIDI_num(num): Search pitch name by pitch number, natural and flat are prior.
            e. g. "C4" for 60.
    """

    __octave = 4

    def __init__(self, pitch: Union[int, str]) -> None:
        self.set(pitch)

    def __str__(self):
        return '{}{}{}'.format(self.__name, '' if self.__accidental == ACCIDENTALS.n.name else self.__accidental,
                                self.__octave)

    def __repr__(self):
        return "Pitch:\n    name: {},\n    number: {},\n    octave: {}".format(str(self), self.number, self.octave)

    def set(self, pitch: Union[int, str]) -> None:
        if(isinstance(pitch, str)):
            pitchName = Pitch.res_name(pitch)
            self.__name = pitchName[0]
            self.__accidental = pitchName[1]
            self.__octave = pitchName[2]
        elif(isinstance(pitch, int)):
            pitchName = Pitch.res_name(Pitch.name_by_MIDI_num(pitch))
            self.__name = pitchName[0]
            self.__accidental = pitchName[1]
            self.__octave = pitchName[2]

    def set_pitch(self, pitch: Union[int, str]) -> None:
        if(self.__octave == 8):
            if(GenericPitch.num_by_name(pitch) > 0):
                raise ValueError("The pitch is out of range, should between A0 and C8")

        super(Pitch, self).set_pitch(pitch)

    def set_octave(self, octave: int) -> None:
        if(octave < 0 or octave > 8):
            raise ValueError("Octave number out of range, should between 0 and 8.")
        elif(octave == 8 and self.number > 0):
            raise ValueError("The pitch is out of range, should between A0 and C8")
        else:
            self.__octave = octave

    def shift(self, interval: interval.GenericInterval, direction: int) -> Pitch:
        pass # TODO

    @staticmethod
    def res_name(pitchName: str) -> tuple:
        """
        Resolve the pitch name with accidental to a tuple and check the format.

        Argument:
            pitchName[str]: The pitch name with accidental e. g. "As4" "C5" "Fds2".

        Return:
            resolvedName[tuple]: Resolved name e. g. ["A", "s", 4].
        """
        octave = int(pitchName[-1])
        genericPitch = GenericPitch.res_name(pitchName[:-1])

        if(octave < 0 or octave > 8):
            raise ValueError("Octave number out of range, should between 0 and 8.")
        elif(octave == 8 and GenericPitch.num_by_name(pitchName[:-1]) > 0):
            raise ValueError("The pitch is out of range, should between A0 and C8")
        else:
            return (genericPitch[0], genericPitch[1], octave)

    @staticmethod
    def name_by_MIDI_num(MIDINum: int) -> str:
        pitchName = GenericPitch.name_by_num(MIDINum % 12)
        octave = MIDINum // 12 - 1
        return "{}{}".format(pitchName, octave)

    @staticmethod
    def names_by_MIDI_num(MIDINum: int) -> str:
        pass #TODO

    @staticmethod
    def MIDI_num_by_name(pitchName: str) -> int:
        pitch = Pitch.res_name(pitchName)
        return GenericPitch.num_by_name("{}{}".format(pitch[0], pitch[1])) + 12 * (pitch[2] + 1)

    @property
    def octave(self):
        return self.__octave
    
    @property
    def MIDInumber(self):
        return Pitch.name_by_MIDI_num(str(self))
    