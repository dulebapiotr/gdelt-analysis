from Session import Session
from typing import Dict, Tuple, Sequence
import pandas as pd
from script import *

quantitative_analysis_dict = {
    'count_events': count_events,
    'event_types_ratio': event_types_ratio,
    'value_in_time': value_in_time,
    'polynomial_fit': polynomial_fit,
    'mean_std_var': get_mean_std_var,
    'median': get_median,
    'range_ptp': get_range_ptp,
    'percentile': get_percentile,
}


def add_analysis(session: Session, data_name: str, analysis: str, params: list) -> Tuple[str, pd.DataFrame]:
    data_dataframe = session.get_data(data_name)
    analysis_func = quantitative_analysis_dict[analysis]
    result_dataframe = analysis_func(data_dataframe)
    result_name = session.add_data(result_dataframe, data_name + analysis)
    return result_name, result_dataframe