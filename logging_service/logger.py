import logging.config
import pathlib
logging.config.fileConfig('logging_service/logger_config.conf')
finance_logger=logging.getLogger("financelogger")
