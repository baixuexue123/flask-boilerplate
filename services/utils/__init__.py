import os
import re


EMAIL_PATTERN = re.compile("^([.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+")


def email_validate(email):
    try:
        return EMAIL_PATTERN.match(email)
    except TypeError:
        return False


def join_media_url(burl, relurl):
    if relurl.startswith('/'):
        relurl = os.path.relpath(relurl, start='/')
    return os.path.join(burl, relurl)
