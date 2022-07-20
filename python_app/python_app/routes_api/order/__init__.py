import logging

logger = logging.getLogger(__name__)
def includeme(config):
    logger.info("Setting routes for routes api")
    config.add_route('order_root', "order")
    config.add_route('order_assessment', "/order/{order_id}")
