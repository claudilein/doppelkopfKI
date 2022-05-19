from enum import Enum


me = "Rumpel"

cardToInt = {
    '10h'   :   0,
    'Dx'    :   1,
    'Dp'    :   2,
    'Dh'    :   3,
    'Dk'    :   4,
    'Bx'    :   5,
    'Bp'    :   6,
    'Bh'    :   7,
    'Bk'    :   8,
    'Ak'    :   9,
    '10k'   :  10,
    'Kk'    :  11,
    '9k'    :  12,
    'Ax'    :  13,
    '10x'   :  14,
    'Kx'    :  15,
    '9x'    :  16,
    'Ap'    :  17,
    '10p'   :  18,
    'Kp'    :  19,
    '9p'    :  20,
    'Ah'    :  21,
    'Kh'    :  22,
    '9h'    :  23
    }

cardPoints = {
    '10h'   :   10,
    'Dx'    :   3,
    'Dp'    :   3,
    'Dh'    :   3,
    'Dk'    :   3,
    'Bx'    :   2,
    'Bp'    :   2,
    'Bh'    :   2,
    'Bk'    :   2,
    'Ak'    :   11,
    '10k'   :  10,
    'Kk'    :  4,
    '9k'    :  0,
    'Ax'    :  11,
    '10x'   :  10,
    'Kx'    :  4,
    '9x'    :  0,
    'Ap'    :  11,
    '10p'   :  10,
    'Kp'    :  4,
    '9p'    :  0,
    'Ah'    :  11,
    'Kh'    :  4,
    '9h'    :  0
    }


intToCard = {
    0   :   '10h',   
    1   :   'Dx',    
    2   :   'Dp',    
    3   :   'Dh',    
    4   :   'Dk',    
    5   :   'Bx',    
    6   :   'Bp',    
    7   :   'Bh',    
    8     :  'Bk',    
    9     :  'Ak',    
    10    :  '10k',  
    11     :  'Kk',    
    12     :  '9k',    
    13     :  'Ax',    
    14     : '10x',  
    15     :  'Kx',    
    16     :  '9x',    
    17     :  'Ap',    
    18     : '10p',   
    19     :  'Kp',    
    20     :  '9p',    
    21     :  'Ah',    
    22     :  'Kh',    
    23     :  '9h' 
    }

class Round(Enum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    ELEVEN = 10
    TWELVE = 11

class Position(Enum):
    FIRST = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3

class Team(Enum):
    NONE = 0
    RE = 1
    KONTRA = 2