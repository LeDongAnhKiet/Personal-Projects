from __future__ import print_function
import argparse
import multiprocessing
import os
import tensorflow as tf
from tensorpack.callbacks.saver import ModelSaver
from tensorpack.train.interface import TrainConfig, launch_train_with_config
from tensorpack.train.trainers import SyncMultiGPUTrainerReplicated
from tensorpack.tfutils.sessinit  import SaverRestore
from tensorpack.utils import logger
from tensorpack.input_source import QueueInput
from load import Net1DataFlow
import hparam as hp
from models import Net1

def train(args, logdir):
    model = Net1()
    df = Net1DataFlow(hp.train1.data_path, hp.train1.batch_size)
    logger.set_logger_dir(logdir)
