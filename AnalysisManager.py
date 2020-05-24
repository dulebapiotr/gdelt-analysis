from Session import Session
from typing import Dict, Tuple, Sequence
import pandas as pd


class AnalysisManager:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AnalysisManager.__instance is None:
            AnalysisManager()
        return AnalysisManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AnalysisManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AnalysisManager.__instance = self

    def add_analysis(self, session: Session, data_name: str, analysis: str) -> Tuple[str, pd.DataFrame]:
        data_dataframe = session.get_data(data_name)
        # analysis_func = tu powinniśmy mieć jakiś słownik funkcji i ich nazw, TODO: zrobić ze script.py
        result_dataframe = None #analysis_func(data_dataframe)  # also ta funkcja przyjmuje jeszcze nazwę kolumny na której operuje
        result_name = session.add_data(result_dataframe, data_name + analysis)
        return result_name, result_dataframe
