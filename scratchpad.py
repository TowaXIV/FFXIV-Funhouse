import logging
import logging.config
import json
import scratchpad2

global timestamp
timestamp = '20231027'
LOG_CONFIG = json.load(open('config/logging/logging.conf', 'r'))
LOG_CONFIG['handlers']['file']['filename'] = f'{timestamp}-logfile.log'

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger(__name__)

logger.info(f'Running {__file__}')
logger.info(f'Activated logger.')
logger.warning('warning test message')
scratchpad2.thing()