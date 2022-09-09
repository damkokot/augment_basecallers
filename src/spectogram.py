#!/usr/bin/env python


### Helper functions to augment and transform input
### Those are: function that creates spectrogram, function to normalize (probably is unecessary)
### functions from SpecAugment methods (only for time masking and frequency masking)
### and fucntion to invert spectrogram to vector 


import torch
import torchaudio
import torchaudio.transforms as T

import numpy as np
import ont



def get_spectrogram(
	event, 
    n_fft=200, 
    win_len=None,
    hop_len=None,
    power=None,
):
    spectrogram = T.Spectrogram(
        n_fft=n_fft,
        win_length=win_len,
        hop_length=hop_len,
        center=True,
        pad_mode="reflect",
        power=power
    )
    spec = spectrogram(event)
    spec = spec.to(torch.float32)
    return spec


def normalize(event):
    """Normalize each event signal using median absolute deviation.
    Method borrowed from Bonito https://github.com/nanoporetech/bonito
    Oxord Nanopore Technologies, Ltd. Public License Version 1.0
    See LICENSE.txt in the bonito repository
    """

    e = event[0]
    signal_start = 0
    signal_end = len(e)
    e_mean = torch.mean(e)
    e_std = torch.std(e)
    e = (e - e_mean) / e_std

    return e


def inv(spec):
    """
    Transoform power units to decibels
    and inverse spectogram to wave form
    """

    spec = spec.to(torch.complex64)

    # inverse
    inv_wv = T.InverseSpectrogram(n_fft=200)
    event = inv_wv(spec, 4096)
    event = event

    return event


def freq_masking(event):
	spec = get_spectrogram(event)
	fm = T.FrequencyMasking(freq_mask_param=5, iid_masks=True)
	spec = fm(spec)
	return spec


def time_masking(event):
    spec = get_spectrogram(event)
    tm = T.TimeMasking(time_mask_param=5)
    spec = tm(spec)

    return spec


def add_noise(event):
    for i, e in enumerate(event):
        e = event[0]
        e = e + 0.009*np.random.normal(0,1,len(e))
        event[i] = e
    return event

