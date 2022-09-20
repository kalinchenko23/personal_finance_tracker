import logging.config
import pathlib
logging.config.fileConfig(f'{pathlib.Path.cwd().parents[0]}/logging_service/logger_config.conf')
finance_logger=logging.getLogger("financelogger")
