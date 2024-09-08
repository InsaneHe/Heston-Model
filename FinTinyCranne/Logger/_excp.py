from __future__ import annotations

from typing_extensions import Literal

__all__ = [
    "UndefinedErrorA",
    "UndefinedErrorB",
    "UndefinedErrorC",
    "UndefinedErrorD",
    "UndefinedErrorE",
    "UndefinedErrorF",
    "UndefinedErrorG",
    "UndefinedErrorH",
    "UndefinedErrorI",
    "UndefinedErrorJ",
    "UndefinedErrorK",
    "UndefinedErrorL",
    "UndefinedErrorM",
    "UndefinedErrorN",
    "UndefinedErrorO",
    "UndefinedErrorP",
    "UndefinedErrorQ",
    "UndefinedErrorR",
    "UndefinedErrorS",
    "UndefinedErrorT",
    "DefaultError"

]


class DefaultError(Exception):
    pass

class UndefinedError(DefaultError):
    message: str
    body: object | None
    """
        预留错误定义消息体
    """

    def __init__(self, message: str, *, body: object | None) -> None:  # noqa: ARG002
        super().__init__(message)
        self.message = message
        self.body = body


class UndefinedErrorT(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorS(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"


class UndefinedErrorR(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorQ(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorP(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorO(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorN(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorM(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorL(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorK(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorJ(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorI(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorH(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorG(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorF(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorE(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorD(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorC(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorB(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

class UndefinedErrorA(UndefinedError):
    """Raised when ................................................"""

    #response:
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message,  body=body)
        #self.response = response
        self.status_code = 0x0000
        self.request_id = "0x000T"

