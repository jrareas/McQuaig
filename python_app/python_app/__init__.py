import logging
from pyramid.config import Configurator
import requests
from asbool import asbool

logger = logging.getLogger(__name__)
def main(global_config, **settings):
    logger.info("Loading Main")
    """ This function returns a Pyramid WSGI application.
    """
    _set_debug(settings)
    with Configurator(settings=settings) as config:
        config.include('.routes_api')
        config.scan()

    register_email_webhook(settings)
    return config.make_wsgi_app()


def register_email_webhook(settings):
    body = {
        "webhook_url": settings.get('email_webhook_url')
        }
    url = f"{settings.get('email_service_url')}/webhook"
    try:
        result = requests.post(url, json=body)
        return result
    except Exception as e:
        print (f"Could not load email webhook: {e}")
    
def _set_debug(settings):
#     import sys
#     sys.path.append('/Applications/Eclipse.app/Contents/Eclipse/plugins/org.python.pydev.core_8.1.0.202012051215/pysrc/pydevd.py')
    
    if settings.get('enable_login') and  asbool(settings['enable_login']) == True:
        import pydevd
        pydevd.settrace('10.254.254.254', port=5678, suspend=False)
        #sys.path.append("")
    