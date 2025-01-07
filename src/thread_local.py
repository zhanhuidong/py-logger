# from . Logger import Logger as Logger
from threading import local
from typing import Any

# logger = Logger._get_logger()
__localInstance = local()


def set(key: str, val: Any) -> None:
    # local()
    # logger.info("set key:{},value:{} ".format(key, val))
    __localInstance.__setattr__(key, val)


def get(key: str) -> Any:
    return __localInstance.__getattribute__(key)


def remove(key: str) -> None:
    __localInstance.__delattr__(key)


def setUserId(userId: Any) -> None:
    set("userId", userId)


def getUserId() -> Any:
    return get("userId")


def setUserName(userName: Any) -> None:
    set("userName", userName)


def getUserName() -> Any:
    return get("userName")

def setDefault():
    set("userId", 0)
    set("userName", "default")
    
def generateTraceId():
    import uuid
    traceId = str(uuid.uuid1()).replace("-", "")
    set("traceId", traceId)
    
def setTraceId(traceId:str):
    set("traceId", traceId)
    
def getTraceId():
    try:
        return get("traceId")
    except Exception as e:
        return '0000'