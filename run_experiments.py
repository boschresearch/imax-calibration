#!/usr/local/bin/python3
# Copyright (c) 2021 Robert Bosch GmbH Copyright holder of the paper "Multi-Class Uncertainty Calibration via Mutual Information Maximization-based Binning" accepted at ICLR 2021.
# All rights reserved.
#
# The paper "Multi-Class Uncertainty Calibration via Mutual Information Maximization-based Binning" accepted at ICLR 2021.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: Kanil Patel
# -*- coding: utf-8 -*-
'''
 run_experiments.py
 imax_calib

 Created by Kanil Patel 
'''
import sys, time
import imax_calib.io as io 
import imax_calib.utils as utils
import numpy as np 
import imax_calib.evaluations.calibration_metrics as calibration_metrics
import imax_calib.calibration as calibration

#################################################### Setup Configutations
cfg = dict(
                # All
                cal_setting="sCW", # CW, sCW or top1
                num_bins=15,
                # Binning
                Q_method="imax",
                Q_binning_stage="raw", # bin the raw logodds or the 'scaled' logodds
                Q_binning_repr_scheme="sample_based",
                Q_bin_repr_during_optim="pred_prob_based",
                Q_rnd_seed=928163,
                Q_init_mode="kmeans",
                )


################################################################################################################################################################################################################################################################################################################
# Start Experiment 
################################################################################################################################################################################################################################################################################################################

data = io.deepdish_read("./data/cifar10_wrn.hdf5")
rnd_indices = np.loadtxt("./data/rnd_indices_1001.csv", delimiter=',').astype(np.int)
num_valid_samples = data["logits"].shape[0]//2

cfg["n_classes"] = data["logits"].shape[1]

valid_logits = data["logits"][rnd_indices[:num_valid_samples]]
valid_labels = data["ytrues"][rnd_indices[:num_valid_samples]]
valid_probs = utils.to_softmax(valid_logits)
valid_logodds = utils.quick_logits_to_logodds(valid_logits, probs=valid_probs)

test_logits = data["logits"][rnd_indices[num_valid_samples:]]
test_labels = data["ytrues"][rnd_indices[num_valid_samples:]]
test_probs = utils.to_softmax(test_logits)
test_logodds = utils.quick_logits_to_logodds(test_logits, probs=test_probs)


calibrator_obj = calibration.learn_calibrator(cfg, 
                                            logits=valid_logits, 
                                            logodds=valid_logodds, 
                                            y=valid_labels, 
                                            )

baseline_obj = calibration.learn_calibrator({**cfg, "Q_method": None}, # get function which does nothing to the data 
                                            logits=valid_logits, 
                                            logodds=valid_logodds, 
                                            y=valid_labels, 
                                            )





# Eval
uncal_logits, uncal_logodds, uncal_probs = baseline_obj(test_logits, test_logodds)
cal_logits, cal_logodds, cal_probs, assigned = calibrator_obj(test_logits, test_logodds)
if cfg["cal_setting"]!="top1":
    multi_cls_labels = test_labels
    uncal_evals = calibration_metrics.compute_top_1_and_CW_ECEs(uncal_probs, multi_cls_labels, list_approximators=["dECE", "mECE"])
    print("Un-calibrated (Baseline): ", uncal_evals)
    cal_evals = calibration_metrics.compute_top_1_and_CW_ECEs(cal_probs, multi_cls_labels, list_approximators=["dECE", "mECE"])
    print("Calibrated: ", cal_evals)
else:
    top1_indices = test_logodds.argmax(axis=-1) 
    correct_c = test_labels[np.arange(top1_indices.shape[0]), top1_indices].astype(np.bool)
    uncal_top1ECE = calibration_metrics.measure_dECE_calibration(uncal_probs[np.arange(top1_indices.shape[0]), top1_indices], correct_c)["ece"]
    print("Un-calibrated (Baseline): Top1ECE: ", uncal_top1ECE)
    cal_top1ECE = calibration_metrics.measure_dECE_calibration(cal_probs, correct_c)["ece"]
    print("Calibrated Top1ECE: ", cal_top1ECE)




print("End Script!")

































