from enum import Enum


class BaseParamDHCPEnum(Enum):
    AutoNetworkParam = 0
    ManualNetworkParam = 1


class BaseParamSummerTimeEnum(Enum):
    UseCorrection = 0
    NotUseCorrection = 1


class BaseParamApbSyncEnum(Enum):
    Local = 0
    Synchronize = 1


class BaseParamBaseModeEnum(Enum):
    Network = 0
    Offline = 1


class ParamEnterVerifyModeEnum(Enum):
    OnlyCard = 0
    CardOrPin = 1
    OnlyPin = 2
    CardAndPin = 3
    OnlyPrint = 4
    PrintOrCard = 5
    PrintAndCard = 6


class ParamPassModeEnum(Enum):
    Standard = 0
    OpenFirstCard = 1
    MiltyPlayer = 2


class InputParamNumEnum(Enum):
    In1 = 1
    In2 = 2
    In3 = 3
    In4 = 4
    REX1 = 5
    REX2 = 6
    REX3 = 7
    REX4 = 8
    AUX_IN1 = 9
    AUX_IN2 = 10
    AUX_IN3 = 11
    AUX_IN4 = 12


class InputParamModeEnum(Enum):
    NotUsed = 0
    NC = 1
    NO = 2
    Reserved = 3
    ReservedNO = 4


class UserAuthorizePassModeEnum(Enum):
    Normal = 0
    Antipassback = 1
    NoOut = 2


class UserAuthorizeInOutEnum(Enum):
    WithIn = 0
    Outside = 1


class HolidayLoopEnum(Enum):
    RepeatEveryYear = 1
    NotRepeatEveryYear = 2


class EventInOutStateEnum(Enum):
    Entrance = 0
    Exit = 1


class EventPriorityEnum(Enum):
    High = 0
    Normal = 1
    Low = 2


class EventTransmittedEnum(Enum):
    InLine = 0
    Confirmed = 1


class InOutFunOutTypeEnum(Enum):
    LockOutputs = 0
    AdditionalOtputs = 1
