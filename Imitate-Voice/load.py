from __future__ import print_function
import argparse
from models import Net2
import numpy as np
from audio import spec_2_wav, inv_premphasis, db_2_amp, denormalize_db
import datetime
import tensorflow as tf
import hparam as hp
from tensorpack.predict.base import OfflinePredictor
from tensorpack.predict.config import PredictConfig
from tensorpack.tfutils.sessinit  import SaverRestore, ChainInit
from tensorpack.callbacks.base import Callback

class Net1DataFlow:
    def __init__(self, data_path, batch_size):
        self.data_path = data_path
        self.batch_size = batch_size
        # Add more initializations as needed

    def get(self):
        # Implement data loading logic here
        data = np.load(self.data_path)
        # Logic to process data into batches of self.batch_size
        return data

class Net2DataFlow:
    def __init__(self, data_path, batch_size):
        self.data_path = data_path
        self.batch_size = batch_size
        # Add more initializations as needed

    def get(self):
        # Implement data loading logic here
        data = np.load(self.data_path)
        # Logic to process data into batches of self.batch_size
        return data

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('case1', type=str, default='case1', help='Case of train1')
    parser.add_argument('case2', type=str, default='case2', help='Case of train2')
    parser.add_argument('-ckpt', help='Checkpoint')
    return parser.parse_args()

def do_convert(args, logdir1, logdir2):

    print(f"Converting using logs {logdir1} and {logdir2}...")

if __name__ == '__main__':
    args = get_arguments()
    hp.set_hparam_yaml(args.case2)
    log1 = '{}/{}/train1'.format(hp.logdir_path, args.case1)
    log2 = '{}/{}/train2'.format(hp.logdir_path, args.case2)
    print('case1: {}, case2: {}, log1: {}, log2: {}'.format(args.case1, args.case2, log1, log2))

    s = datetime.datetime.now()
    do_convert(args, logdir1=log1, logdir2=log2)
    print('Done in {}s'.format((datetime.datetime.now() - s).seconds))