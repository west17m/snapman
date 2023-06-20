#!/usr/bin/env python3
import logging
import os
import re
import json
import math
import time
from subprocess import Popen, PIPE
import numpy as np
import pandas as pd

LOG_FILE='server-setup.log'

# logging
# @todo support logging configuration file
def configure_logging():
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE,
                    filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)


# takes string input and outputs an array
def cmd_to_array(cmd):
    logging.debug('tokenizing cmd ' + cmd)
    ca=[]
    # this explodes on spaces but preserves quoted strings
    for token in re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', cmd):
        ca.append(token)

    logging.debug('returning ' + str(ca))
    return(ca)

# run cmd, log output, throw and error if return code is not 0
def shell(cmd,log_output=True):
    logging.debug('request to run command: ' + cmd)
    p = Popen(cmd_to_array(cmd), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out = p.stdout.read()
    err = p.stderr.read().decode()
    if log_output:
        logging.debug(out)
    streamdata = p.communicate()[0]
    rc = p.returncode
    logging.debug('return code: ' + str(rc))
    if rc != 0:
        msg = 'the following command was not executed successfully ' + cmd + ' ' + str(err)
        logging.error(msg)
        raise RuntimeError(msg)

    return out

def get_snaps(dataset=''):

    # @todo validate dataset
    # @todo cache
    out = shell('zfs list -t snapshot -o name -s name ' + dataset)
    return pd.Series(out.splitlines(),dtype=str)

def get_auto_snaps(label,dataset=''):
    return snaps[snaps.str.endswith(label)]


start_time = time.time()

dataset = 'tank'
snaps = get_snaps(dataset)
print("--- %s seconds ---" % (time.time() - start_time))

for label in ['frequent','hourly','daily','weekly','monthly']:
    print(label + ' ' + str(len(get_auto_snaps(label,dataset))))

print(dataset + ' snapshots ' + str(len(snaps)))

print("--- %s seconds ---" % (time.time() - start_time))
