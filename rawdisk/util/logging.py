import logging.config
import yaml
import os

def setup_logging(config_path=None, log_level=logging.INFO, formatter='standard'):
    """Setup logging configuration
    """

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format':
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'cli': {
                'format':
                    '[%(levelname)s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': formatter,
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': True
            },
            'yapsy': {
                'handlers': ['console'],
                'level': logging.INFO
            }
        }
    }

    if config_path:
        if os.path.exists(config_path):
            with open(config_path, 'rt') as f:
                config = yaml.safe_load(f.read())
        else:
            print('Specified path does not exist: {}, '
                  'using default config'.format(config_path))

    logging.config.dictConfig(config)
