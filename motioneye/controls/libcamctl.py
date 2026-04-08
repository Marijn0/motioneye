from logging import debug
import re
from shutil import which
from subprocess import CalledProcessError

from motioneye import utils


def list_devices():
    debug('detecting libcamera camera')

    binary = which('libcamera-hello') or which('rpicam-hello')
    if not binary:
        debug(
            'unable to detect libcamera camera: no libcamera-hello or rpicam-hello binary found'
        )
        return []

    try:
        output = utils.call_subprocess([binary, '--list-cameras'], stderr=utils.DEV_NULL)

    except CalledProcessError:
        debug('unable to detect libcamera camera: "--list-cameras" failed')
        return []

    if 'no cameras available' in output.lower():
        debug('no libcamera cameras detected')
        return []

    for line in output.splitlines():
        line = line.strip()
        if not re.match(r'^\d+\s*:', line):
            continue

        name = re.sub(r'^\d+\s*:\s*', '', line).strip()
        if not name:
            name = 'libcamera Camera'

        return [('camera0', name)]

    if output:
        debug('libcamera camera detected')
        return [('camera0', 'libcamera Camera')]

    return []
