import logging

LOGGER_NAME = "dzengi_com_client"
_DEFAULT_LOG_FORMAT = "%(name)s %(levelname)s %(message)s"


def _has_real_handler(logger):
    return any(not isinstance(handler, logging.NullHandler) for handler in logger.handlers)


def get_sdk_logger(logger=None, debug: bool = False):
    sdk_logger = logger or logging.getLogger(LOGGER_NAME)

    if logger is None and not any(isinstance(handler, logging.NullHandler) for handler in sdk_logger.handlers):
        sdk_logger.addHandler(logging.NullHandler())

    if logger is None:
        if debug and not _has_real_handler(sdk_logger):
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(_DEFAULT_LOG_FORMAT))
            sdk_logger.addHandler(handler)
            sdk_logger.propagate = False

    if debug:
        sdk_logger.setLevel(logging.DEBUG)

    return sdk_logger
