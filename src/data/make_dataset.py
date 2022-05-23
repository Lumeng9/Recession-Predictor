"""
This module gets data from FRED and Yahoo Finance, builds some features,
and saves the data into the respective filepaths.
"""

import json
from datetime import datetime

import pandas as pd
import requests as req
from fredapi import fred, Fred

import RecessionPredictor_paths as path


class DataSeries:
    """
    Contains methods and objects to retrieve data from FRED and Yahoo Finance.
    """
    
    def __init__(self):
        self.dates = []
        self.values = []

    def fred_response(self, params):
        """
        Makes requests to the FRED API.
        
        params: dictionary, FRED API parameters.
        """
        params = dict(params)
        data = pd.DataFrame()
        fred_request = req.get(url='https://api.stlouisfed.org/fred/series/observations',
                               params=params)
        fred_json = json.loads(fred_request.text)['observations']
        for observation in fred_json:
            self.dates.append(str(observation['date']))
            self.values.append(float(observation['value']))


class MakeDataset:
    """
    The manager class for this module.
    """
    
    def __init__(self):
        """
        fred_series_ids: identifiers for FRED data series.
        
        yahoo series_ids: identifiers for Yahoo Finance data series.
        """
        self.primary_dictionary_output = pd.DataFrame()
        self.primary_df_output = pd.DataFrame()
        self.shortest_series_name = ''
        self.shortest_series_length = 1000000

    def get_fred_data(self, series_key):
        """
        Cycles through "fred_series"ids" to get data from the FRED API.
        """
        import time
        
        now = datetime.now()
        month = now.strftime('%m')
        year = now.year
        day = now.day
        most_recent_date = '{}-{}-{}'.format(year, month, day)
        fred = Fred(api_key=path.fred_api_key)
        print('\nGetting data from FRED API as of {}...'.format(most_recent_date))

        self.primary_dictionary_output['10Y_Treasury_Rate'] = fred.get_series(series_key)
        print('Finished getting data from FRED API!')
        return self.primary_dictionary_output

    def get_primary_data(self, series_key):
        """
        Gets primary data from FRED API and Yahoo Finance.
        """
        
        print('\nGetting primary data from APIs...')
        out_df = self.get_fred_data(series_key)
        return out_df

    def get_all_data(self, series_key):
        """
        Gets data from primary sources (FRED and Yahoo Finance), then performs
        preliminary manipulations before saving the data.
        """
        out_df = self.get_primary_data(series_key)
        # Fill NaN value with the mean of the previous and the next row
        out_df = out_df.interpolate()
        return out_df


# FRED citations
#U.S. Bureau of Labor Statistics, All Employees: Total Nonfarm Payrolls [PAYEMS], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/PAYEMS
#U.S. Bureau of Labor Statistics, Civilian Unemployment Rate [UNRATE], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/UNRATE
#Board of Governors of the Federal Reserve System (US), Effective Federal Funds Rate [FEDFUNDS], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/FEDFUNDS
#U.S. Bureau of Labor Statistics, Consumer Price Index for All Urban Consumers: All Items [CPIAUCSL], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/CPIAUCSL
#Board of Governors of the Federal Reserve System (US), 10-Year Treasury Constant Maturity Rate [GS10], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/GS10
#Board of Governors of the Federal Reserve System (US), 5-Year Treasury Constant Maturity Rate [GS5], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/GS5
#Board of Governors of the Federal Reserve System (US), 3-Month Treasury Bill: Secondary Market Rate [TB3MS], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/TB3MS
#Board of Governors of the Federal Reserve System (US), Industrial Production Index [INDPRO], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/INDPRO
        
#MIT License
#
#Copyright (c) 2019 Terrence Zhang
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.