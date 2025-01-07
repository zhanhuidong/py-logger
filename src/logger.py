from .LoggerHandler import CommonTimedRotatingFileHandler
from . import thread_local 
import logging
import logging.handlers
import os
import socket
import sys
import time
from datetime import datetime, timezone, timedelta

server_name = os.getenv('server.name', 'common-log')
server_logging_path = os.getenv('server.logging.path', '/apps/logs')

class LoggerFormatter(logging.Formatter):
    
    def format(self, record):
        record.traceId = thread_local.getTraceId()
        ss = logging.Formatter.format(self, record)
        return ss

class MessageFormatter(logging.Formatter):
    
    def format(self, record):
        record.traceId = thread_local.getTraceId()
        record.timestamp = get_current_iso()
        
        return logging.Formatter.format(self, record)
    
    def formatMessage(self, record):
        record.message = record.message.replace('{', '【').replace('}', '】').replace('"', '``').replace("'", '`')
        return super().formatMessage(record)

def get_current_iso():
    
    # 获取当前时间
    current_time = datetime.now(timezone(timedelta(hours=8)))

    # 格式化时间为ISO 8601格式
    formatted_time = current_time.isoformat()
    return formatted_time

'''
日志模块
'''   
hostname = socket.gethostname()
rq = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
log_date = rq[:10]
if not os.path.exists(f"{server_logging_path}/{server_name}"):
    os.makedirs(f"{server_logging_path}/{server_name}", exist_ok=True)
LOG_FILENAME = f'{server_logging_path}/{server_name}/{server_name}-{hostname}.log'
JSON_FILENAME = f'{server_logging_path}/{server_name}/{server_name}-{hostname}.json'
fmt = LoggerFormatter('[%(traceId)s][%(threadName)s][%(funcName)s][%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Logger:
    
    logInstance = None

    @staticmethod
    def _get_logger():
        if Logger.logInstance is not None:
            return Logger.logInstance
        # logging.basicConfig(filename=LOG_FILENAME, encoding='utf-8', level=logging.INFO)
        log = logging.getLogger("")
        log.setLevel(logging.INFO)
        # console
        console_handle = logging.StreamHandler(sys.stdout)
        console_handle.setFormatter(fmt)
        console_handle.setLevel(logging.INFO)

        # file
        # file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when='D', interval=1, backupCount=365, encoding="utf-8")
        file_handler = CommonTimedRotatingFileHandler(LOG_FILENAME, backupCount=7, encoding="utf-8", when='D')
        file_handler.setFormatter(fmt)
        file_handler.setLevel(logging.INFO)

        # json
        # json_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when='D', interval=1, backupCount=365, encoding="utf-8")
        json_handler = CommonTimedRotatingFileHandler(JSON_FILENAME, backupCount=7, encoding="utf-8", when='D')
        fmt_json = '{"@timestamp" : "%(timestamp)s", "traceId": "%(traceId)s","threadName":"%(threadName)s", "funcName":"%(funcName)s", "asctime": "%(asctime)s","service": "'+server_name+'", "filename": "%(filename)s", "line": "%(lineno)d", "levelname": "%(levelname)s", "message": "%(message)s"}'
        # json_fmatter.formatMessage()
        # json_handler.setFormatter(StrFormatter(fmt_json))
        # json_handler.setFormatter(logging.Formatter(fmt_json))
        json_handler.setFormatter(MessageFormatter(fmt_json))
        json_handler.setLevel(logging.INFO)

        log.addHandler(file_handler)
        log.addHandler(console_handle)
        log.addHandler(json_handler)
        
        Logger.logInstance = log
        return Logger.logInstance