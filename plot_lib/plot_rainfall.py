import math
import os
import numpy as np
import pandas as pd
from typing import Optional, Any, Union

script_dir = os.path.abspath('../')

custom_dir = '../assets'
dir_script = '../assets/results/'


def integrate_datetime(df, sum: Optional[bool] = True):
    date = pd.to_datetime(df[['year', 'month', 'day']])
    date = date.dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
    df['date'] = date
    df['english_day'] = df.date.dt.strftime('%a')
    df = df.sort_values(by='date')
    df = df.reset_index()
    if not sum:
        return df
    df['sum'] = df['sum'].astype(float)
    return df


class RainGauge:
    def __init__(
            self,
            root_asset: Optional[str] = dir_script,
            path_concat: Optional[str] = dir_script
    ):
        """

        :param root_asset:
        """
        self.root_asset = os.path.join(custom_dir, root_asset)
        self.path_concat = os.path.join(custom_dir, path_concat)

    def df_interpolate_nan(self, path: str, rainfall: Any = None):
        """

        :param path:
        :param rainfall:
        :return:
        """

        df = pd.read_excel(self.root_asset + path)
        df = df.drop(['Unnamed: 0'], axis=1)
        df = df.replace('-', 0, regex=True)
        if rainfall:
            df[rainfall] = df[rainfall].replace(np.nan, 0)
            df = df.replace(np.nan, '')
            return df
        df['sum'] = df['sum'].replace(np.nan, 0)
        df = df.replace(np.nan, '')
        return df

    @staticmethod
    def add_column_split_datetime(df: Any = None):
        """

        :param df:
        :return:
        """

        if df is None:
            return df
        date = pd.to_datetime(df[['year', 'month', 'day']])
        date = date.dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
        df['date'] = date
        df['english_day'] = df.date.dt.strftime('%a')
        return df

    def concat(self, filename: Union[str, None] = 'concatfile.xlsx') -> None:
        concat = []
        for fn in os.listdir(self.path_concat):
            if not fn.startswith('.'):
                path_fn = os.path.join(self.path_concat, fn)
                df = pd.read_csv(path_fn)
                concat.append(df)

        df = pd.concat(concat)
        df.to_excel(filename, engine='xlsxwriter')

    @staticmethod
    def filter_dates(
            df,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            year: Optional[int] = 2020
    ):
        if start_date and end_date:
            after_start_date = df['date'] >= start_date
            before_end_date = df['date'] <= end_date
            between_two_dates = after_start_date & before_end_date
            filtered_dates = df.loc[between_two_dates]
            return filtered_dates
        return df.loc[df['year'] == year]
