import time

from celery.utils.log import get_task_logger

from services.app import celery

logger = get_task_logger(__name__)


@celery.task(name='log.log_request', ignore_result=True)
def log_request(**kwargs):
    logger.info('log_request:%s', time.time())
