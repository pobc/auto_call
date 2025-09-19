from enum import Enum


class CustomLevel(Enum):
    MISSED=-1
    OK = 1
    MAYBE = 2
    REJECT = 3
    UNKNOWN = 4


class PhoneState(Enum):
    CHATTING = 'chatting'
    FREE = 'free'
    RINGING = 'ringing'
    CALLING = 'calling'
    UNKNOWN = 'unknown'


if __name__ == '__main__':
    print(CustomLevel.OK.name)
    print(CustomLevel.UNKNOWN.value)
