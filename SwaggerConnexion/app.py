#!/usr/bin/env python3
import connexion
import logging
import time
from random import randint
from time import sleep
from connexion import NoContent

# our memory-only device storage
DEVICES = {}

def get_devices(limit, device_type=None):
    return [device for device in DEVICES.values() if not device_type or device['device_type'] == device_type][:limit]

def get_device(device_id):
    device = DEVICES.get(device_id)
    sleep(5)
    #sleep(randint(0,10))
    return device or ('Not found', 404)


def put_device(device_id, device):
    exists = device_id in DEVICES
    device['id'] = device_id
    if exists:
        logging.info('Updating device %s..', device_id)
        DEVICES[device_id].update(device)
    else:
        logging.info('Creating device %s..', device_id)
        DEVICES[device_id] = device
    return NoContent, (200 if exists else 201)


def delete_device(device_id):
    if device_id in DEVICES:
        logging.info('Deleting device %s..', device_id)
        del DEVICES[device_id]
        return NoContent, 204
    else:
        return NoContent, 404


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('networkdevices_swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
