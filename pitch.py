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
""" Last modified: 2021-06-06                                                        """
"""                                                                                  """
""" Description: Defined all the attributes and operations of pitches without modes  """
"""              and scales.                                                         """
"""                                                                                  """
""" Exported classes:                                                                """
"""     PITCHES(Enum), ACCIDENTALS(Enum), GenericPitch, Pitch                        """

from enum import Enum
from typing import Union
import interval

# Pitch names constant defination
class PITCHES(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11


# Accidental names constant defination
class ACCIDENTALS(Enum):
    df = -2 # Double Flat
    f = -1 # Flat
    n = 0 # Natural
    s = 1 # Sharp
    ds = 2 # Double Sharp


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
        add[GenericPitch + AbstractInterval]: Raise the pitch with an interval.
            e. g. "C + M3 = E" //Pseudo code, not Python
        sub[GenericPitch - AbstractInterval]: Lower the pitch with an interval.
            e. g. "C - M3 = Ab"
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
            pitchname = GenericPitch.res_name(pitch)
            self.__name = pitchname[0]
            self.__accidental = pitchname[1]
        elif(isinstance(pitch, int)):
            pitchname = GenericPitch.name_by_num(pitch)
            self.__name = pitchname[0]
            self.__accidental = pitchname[1]

    def set(self, pitch: Union[int, str]) -> None:
        """
        Set this instance with pitch name or pitch number.

        Arguments:
            pitch[int: 0-11]: The pitch number, "0-12" corresponding to pitch name "C-B". Natural and flat pitches are prior.
            or pitch[str: member of "PITCHES"]: The pitch name, using this kind of argument is recommonded.
        """
        self.set_pitch(pitch)

    def shift(self, interval: interval.AbstractInterval, direction):
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
        pitchNumber = self.number + direction * interval.size
        utils.constrain_by_cycle(pitchNumber, 0, 12)
        '''if(pitchNumber < 0):
            pitchNumber += 12
        elif(pitchNumber > 11):
            pitchNumber -= 12'''

        # find possible pitch name
        shiftedPitchName = ord(self.__name) + direction * (int(interval.name[1]) - 1)
        shiftedPitchName = chr(utils.constrain_by_cycle(shiftedPitchName, 65, 8))
        '''if(shiftedPitchName < 65): # ASCII 65: A
            shiftedPitchName += 7
        elif(shiftedPitchName > 71):# ASCII 71: G
            shiftedPitchName -= 7
        shiftedPitchName = chr(shiftedPitchName)'''

        pitchNames = GenericPitch.names_by_num(pitchNumber)
        for pitchName in pitchNames:
            if(shiftedPitchName == pitchName[0]):
                return GenericPitch(pitchName)

        # enharmonic if no found
        return GenericPitch(pitchNames[int(1 - direction / 2)])

    @staticmethod
    def res_name(pitname: str) -> tuple:
        # check argument
        if(pitname[0] in PITCHES.__members__):
            name = pitname[0]
        else:
            raise ValueError('Pitch name must be one of "C", "D", "E", "F", "G", "A", "B".')

        if(len(pitname) == 1):
            accidental = ACCIDENTALS.n.name
        elif(pitname[1:] in ACCIDENTALS.__members__):
            accidental = pitname[1:]
        else:
            raise ValueError('The accidental of pitch name must be one of "s", "f", "ds", "df", or "n".')

        return (name, accidental)

    @staticmethod
    def num_by_name(name: str) -> int:
        name = GenericPitch.res_name(name)
        return (PITCHES[name[0]].value + ACCIDENTALS[name[1:]].value) % 12

    @staticmethod
    def names_by_num(num: int) -> List:
        # check argument
        if(not(0 <= num < 12)):
            raise ValueError('Pitch number must be an integer between 0 and 11.')

        names = []
        try:
            names.apppend(PITCHES(num).name, ACCIDENTALS.n.name)
        pass #TODO(Luo Zhong-qi): Waiting for realize...

    @staticmethod
    def name_by_num(num: int) -> str:
        if(not(0 <= num < 12)):
            raise ValueError('Pitch number must be an integer between 0 and 11.')

        try:
            return (PITCHES(num).name, ACCIDENTALS.n.name)
        except:
            return (PITCHES(num + 1).name, ACCIDENTALS.df.name)


    #def __add__(self, interval: AbstractInterval) -> GenericPitch: # ERROR
    def __add__(self, interval):
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

    #def __sub__(self, interval: AbstractInterval) -> GenericPitch: # ERROR
    def __sub__(self, interval):
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
        return (PITCHES[self.__name].value + ACCIDENTALS[self.__accidental].value) % 12
    

class Pitch(GenericPitch):
    pass