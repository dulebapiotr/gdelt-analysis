import traceback

from Session import Session
from typing import Dict, Tuple, Sequence
import pandas as pd
from analyses import *

quantitative_analysis_dict = {
    'count_events': count_events,
    'event_types_ratio': event_types_ratio,
    'polynomial_fit': polynomial_fit,
    'polynomial_fit_df': polynomial_fit_df,
    'mean_std_var': get_mean_std_var_df,
    'median': get_median,
    'median_df': get_median_df,
    'range_ptp': get_range_ptp,
    'percentile': get_percentile,
    'percentile_df': get_percentile_df,
    'filter': filter_events_relation,
}


def add_analysis(session: Session, data_name: str, analysis: str, params: Dict[str, any]):
    data_dataframe = session.get_data(data_name)
    analysis_func = quantitative_analysis_dict[analysis]
    try:
        result_df = analysis_func(data_dataframe, params)
        result_name = session.add_data(result_df, data_name + analysis)
        return result_df.to_json()
    except ValueError:
        traceback.print_exc()
        # todo: change to error 400
        return "invalid argument", {}
