import loggingimport logging.handlersimport logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('test')

#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='test.log',filemode='w')
#LOG_FILE = 'test.log'
#console = logging.StreamHandler()
#console.setLevel(logging.INFO)
#formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)





logger.debug('This is debug message')logger.info('This is info message')logger.warning('This is warning message')
