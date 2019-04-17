import multiprocessing

daemon = True

reload = False

user = "admin"
group = "admin"

raw_env = "FLASK_ENV=testing"

bind = "127.0.0.1:8000"

worker_class = "gevent"

workers = multiprocessing.cpu_count()

threads = multiprocessing.cpu_count() * 2

max_requests = 2000

backlog = 2048

proc_name = 'gunicorn'

loglevel = 'info'
pidfile = './logs/gunicorn.pid'

logfile = './logs/gunicorn.log'

accesslog = './logs/gunicorn.access.log'
access_log_format = '%(h)s %(l)s %(t)s "%(r)s" %(s)s %(D)s'

errorlog = './logs/gunicorn.error.log'

# gunicorn -c gun.py  wsgi:app
