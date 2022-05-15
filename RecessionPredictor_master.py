"""
This is the main script that runs all modules.
"""

import os
import argparse

os.chdir(os.path.dirname(os.path.abspath(__file__))) 
import src.data.make_dataset as mk
import src.features.build_features_and_labels as ft
import src.visualization.exploratory_analysis as exp
import src.models.testing as test
import src.visualization.test_results as test_results
import src.models.deployment as deploy
import src.visualization.deployment_results as deploy_results

#
# parser = argparse.ArgumentParser()
# parser.add_argument('process', type=str,
#                     default='deploy',
#                     help=
#                     """
#                     Which process would you like to run? Choices are "backtest"
#                     or "deploy".
#                     """,
#                     choices=['backtest', 'deploy'])
# args = parser.parse_args()
process = 'deploy'

# please choose between 'T10Y2Y' and 'T10Y3M'
series_key = 'T10Y2Y'

if process == 'backtest':
   data = mk.MakeDataset().get_all_data(series_key)
   fd = ft.FinalizeDataset(data)
   fd.create_final_dataset()
   explore_data = exp.ExploratoryAnalysis().explore_dataset()
   backtest = test.Backtester().run_test_procedures()
   plot_backtest = test_results.TestResultPlots().plot_test_results()
    
elif process == 'deploy':
   data = mk.MakeDataset().get_all_data(series_key)
   fd = ft.FinalizeDataset(data)
   fd.create_final_dataset()
   deploy = deploy.Deployer().run_test_procedures()
   plot_deploy = deploy_results.TestResultPlots().plot_test_results()
   

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
