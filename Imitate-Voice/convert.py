from __future__ import print_function
import argparse
from models import Net2
import numpy as np
from audio import spec_2_wav, inv_premphasis, db_2_amp, denormalize_db
import datetime
import tensorflow as tf
from hparam import hparam as hp
from load import Net2DataFlow
from tensorpack.predict.base import OfflinePredictor
from tensorpack.predict.config import PredictConfig
from tensorpack.tfutils.sessinit  import SaverRestore, ChainInit
from tensorpack.callbacks.base import Callback

def convert(predictor, df):
    pred, y, ppgs = predictor(next(df().get()))
    pred = denormalize_db(pred, hp.default.max_db, hp.default.min_db)
    y = denormalize_db(y, hp.default.max_db, hp.default.min_db)

    pred = np.power(db_2_amp(pred), hp.convert.emphasis_magnitude)
    y = np.power(db_2_amp(y), hp.convert.emphasis_magnitude)
    audio = np.array(map(lambda spec: spec_2_wav(spec.T, hp.default.n_fft, hp.default.win_length,
                                                 hp.default.hop_length, hp.default.n_iter, pred)))
    y = np.array(map(lambda spec: spec_2_wav(spec.T, hp.default.n_fft, hp.default.win_length,
                                                 hp.default.hop_length, hp.default.n_iter, y)))

    audio = inv_premphasis(audio, coeff = hp.default.preemphasis)
    y = inv_premphasis(y, coeff = hp.default.preemphasis)
    return audio, y, ppgs

def get_eval_inputs():
    return ['x_mfcss', 'y_specs', 'y_mel']
