import multiprocessing

daemon = True

reload = False

user = "admin"
group = "admin"

# chdir = ""

raw_env = "FLASK_ENV=testing"

bind = "127.0.0.1:8000"

worker_class = "gevent"

workers = multiprocessing.cpu_count()

threads = multiprocessing.cpu_count() * 2

max_connections = 1000

max_requests = 2000

backlog = 1024

proc_name = 'xxx'

loglevel = 'info'
pidfile = './logs/gunicorn.pid'

logfile = './logs/gunicorn.log'

accesslog = './logs/gunicorn.access.log'
access_log_format = '%(h)s %(l)s %(t)s "%(r)s" %(s)s %(D)s'

errorlog = './logs/gunicorn.error.log'
