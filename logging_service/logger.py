import logging.config
import pathlib
logging.config.fileConfig('/Users/maximkalinchenko/Desktop/personal_finance_tracker/logging_service/logger_config.conf')
finance_logger=logging.getLogger("financelogger")
