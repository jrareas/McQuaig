import logging

logger = logging.getLogger(__name__)
def includeme(config):
    config.include('.geoip')
