import logging.config
import pathlib
logging.config.fileConfig('/home/ubuntu/personal_finance_tracker/backend/logging_service/logger_config.conf')
finance_logger=logging.getLogger("financelogger")
