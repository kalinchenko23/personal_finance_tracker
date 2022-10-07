import logging.config
import pathlib
logging.config.fileConfig(f'{pathlib.Path(__file__).parents[0]}/logger_config.conf')
finance_logger=logging.getLogger("financelogger")
