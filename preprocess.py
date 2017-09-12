# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.utils import exist, load_json, dump_json
from ppg.signal import smooth_ppg_signal, extract_ppg_single_waveform


def preprocess():
    segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')
    preprocessed_data_dir = os.path.join(BASE_DIR, 'data', 'preprocessed')

    if exist(pathname=segmented_data_dir):
        for filename_with_ext in fnmatch.filter(os.listdir(segmented_data_dir), '*.json'):
            pathname = os.path.join(segmented_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for session_id in json_data:
                    if json_data[session_id]['rest']['ppg']['signal'] is not None:
                        json_data[session_id]['rest']['ppg']['single_waveforms'] = extract_ppg_single_waveform(signal=smooth_ppg_signal(signal=json_data[session_id]['rest']['ppg']['signal'], sample_rate=json_data[session_id]['rest']['ppg']['sample_rate']))
                    else:
                        json_data[session_id]['rest']['ppg']['single_waveforms'] = None
                    del json_data[session_id]['rest']['ppg']['signal']
                    for block in json_data[session_id]['blocks']:
                        if block['ppg']['signal'] is not None:
                            block['ppg']['single_waveforms'] = extract_ppg_single_waveform(signal=smooth_ppg_signal(signal=block['ppg']['signal'], sample_rate=block['ppg']['sample_rate']))
                        else:
                            block['ppg']['single_waveforms'] = None
                        del block['ppg']['signal']
                dump_json(data=json_data, pathname=os.path.join(preprocessed_data_dir, filename_with_ext), overwrite=True)


if __name__ == '__main__':
    preprocess()