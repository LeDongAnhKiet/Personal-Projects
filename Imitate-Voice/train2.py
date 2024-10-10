import tensorflow as tf
from tensorpack.callbacks.saver import ModelSaver
from tensorpack.train.interface import TrainConfig, launch_train_with_config
from tensorpack.train.trainers import SyncMultiGPUTrainerReplicated
from tensorpack.tfutils.sessinit import SaverRestore
from tensorpack.utils import logger
from tensorpack.input_source.input_source import QueueInput
from load import Net2DataFlow
import hparam as hp
from models import Net2

def train(args, logdir):
    model = Net2()
    df = Net2DataFlow(hp.train2.data_path, hp.train2.batch_size)
    logger.set_logger_dir(logdir)
    
    config = TrainConfig(
        model=model,
        data=QueueInput(df),
        callbacks=[ModelSaver()],
        steps_per_epoch=1000,
        max_epoch=10,
    )
    launch_train_with_config(config, SyncMultiGPUTrainerReplicated(args.num_gpus))
