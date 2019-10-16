import logging
import sys, os
from datetime import datetime

fileLoc = os.path.split(sys.argv[0])[-1]
logging.basicConfig(filename='logs/{:%Y-%m-%d}.log'.format(datetime.now()), filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(fileLoc)
logger.setLevel(logging.DEBUG)