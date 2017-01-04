#!/usr/bin/env python3
import connexion
import logging
import time
from random import randint
from time import sleep
from Config import Constants
from connexion import NoContent
from random import choice
from string import digits

# our memory-only device storage
IPCHDR = {}

def ipc(limit):
    return [IpcHdr for IpcHdr in IPCHDR.values()][:limit]


def put_ipc(IpcHdr):
    tid = ''.join(choice(digits) for i in range(5))
    exists = tid in IPCHDR
    IpcHdr['tid'] = tid
    if exists:
        logging.info('Updating %s..', tid)
        IPCHDR[tid].update(IpcHdr)
    else:
        logging.info('Creating %s..', tid)
        IPCHDR[tid] = IpcHdr
    return NoContent, (200 if exists else 201)


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
#app.add_api('networkdevices_swagger.yaml')
app.add_api(Constants.swaggerFile)
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
