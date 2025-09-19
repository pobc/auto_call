import logging
import sys
import time

import main.config as config
from logging.handlers import TimedRotatingFileHandler

ce_logger = logging.getLogger()
log_format_str = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
ce_logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename=config.log_path, when="midnight", interval=1, encoding='utf-8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(logging.Formatter(log_format_str))
ce_logger.addHandler(handler)
if config.local_mode:
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    logFormatter = logging.Formatter(log_format_str)
    consoleHandler.setFormatter(logFormatter)
    ce_logger.addHandler(consoleHandler)


def get_logger():
    return ce_logger


if __name__ == '__main__':
    print(12344)
    for i in range(100):
        ce_logger.info("123")
        get_logger().debug("123")
        get_logger().error("123")
        time.sleep(20)
