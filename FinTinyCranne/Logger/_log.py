import os
import logging

logger: logging.Logger = logging.getLogger("FinancialTinyCranne")
finx_logger: logging.Logger = logging.getLogger("finx")


def _basic_config() -> None:
    # e.g. [2000-01-05 14:12:26 - anthropic._base_client:818 - DEBUG] HTTP Request: POST http://127.0.0.1:4010/foo/bar "200 OK"
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def setup_logging() -> None:
    env = os.environ.get("ANTHROPIC_LOG")
    if env == "debug":
        _basic_config()
        logger.setLevel(logging.DEBUG)
        finx_logger.setLevel(logging.DEBUG)
    elif env == "info":
        _basic_config()
        logger.setLevel(logging.INFO)
        finx_logger.setLevel(logging.INFO)