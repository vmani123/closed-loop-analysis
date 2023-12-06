from utilities.posthoc_utils import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



input_files = st.file_uploader('load your dlc file', accept_multiple_files=True)
try:
    df = pd.read_csv(input_files[0])
    if st.button('start analysis'):
        csv_array_filtered, perc_filtered = adp_filt(df, np.arange(18))
        col1, col2 = st.columns(2)

        start = col1.number_input('time start in seconds', min_value=0, max_value=None)
        stop = col2.number_input('time stop in seconds', min_value=0, max_value=None)
        if stop <= start:
            st.error('STOP HAS TO BE GREATER THAN START')
        else:
            behavior_dict = {0: 'left', 1:'right', 2:'locomotion', 3:'face groom', 4:'other groom', 5:'all other'}
            behavior_choice = st.number_input(f'choose behavior {behavior_dict}', min_value=0, max_value=5)
            st.success(f'you have chosen {behavior_dict[behavior_choice]}')

            file_num = len(input_files)
            fig, ax = plt.subplots(1, 1, figsize=(4, 3))
            fig.suptitle('realtime stim')
            ax.plot(np.arange(len(time_since)), time_since)

            ax.set_xlabel('count')
            ax.set_ylabel('time since start (s)')
            ax.hlines(start, 0, len(time_since), ls='--', color='k')
            ax.hlines(stop, 0, len(time_since), ls='--', color='r')
            colfig, colsummary = st.columns([2, 1])

            colfig.pyplot(fig)
            colsummary_exp = colsummary.expander('Summary statistics', expanded=True)
            colsummary_exp.write(f'{behavior_dict[behavior_choice]} from {start}s-{stop}s '
                     f'has {time_since[(time_since > start) & (time_since < stop)].shape[0]} bouts')


except IndexError:
    st.warning('please upload file')



