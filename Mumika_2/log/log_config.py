from .utils import get_default_log_path

DEFAULT_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'app_error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': get_default_log_path('app_error.log'),
            'maxBytes': 1024*1024*16, # 16 MB
            'backupCount': 10,
            'formatter': 'simple',
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'app_error_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}