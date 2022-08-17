import hashlib

@celery.task
def md5sum(path):
    return hashlib.md5(open(path,'rb').read()).hexdigest()