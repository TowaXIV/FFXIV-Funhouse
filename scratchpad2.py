import logging
def thing():
    logger = logging.getLogger(__name__)

    logger.info(f'Activated logger in {__name__}.')
    logger.warning('This file was not done past the deadline.')