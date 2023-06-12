# Import dependencies

from directories import log_config, log_func, data_dir, covariates, thickness, volume, output_dir, nj
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import warnings
import networkx as nx
from scipy import stats
from sklearn.linear_model import LinearRegression
import logging
import argparse

log_config()
	
#-----------------------------------------------------------------------------------------------------------------


# Correct for covariates

def covar_correct(X, Y, data, n_jobs=1):
    
    def get_resid(X, y, data, n_jobs=n_jobs):
        r = data[y] - LinearRegression(n_jobs=n_jobs).fit(data[X], data[y]).predict(data[X])
        return r
    
    R = Parallel(n_jobs=n_jobs)(delayed(get_resid)(X, y, data, n_jobs=n_jobs) for y in Y)
    return np.asanyarray(R).T

demographics = pd.read_csv(f"{data_dir}/Demographics.csv", index_col="SubjID")
thickness_volume = pd.read_csv(f"{data_dir}/CT_Volume.csv", index_col="SubjID")
brain_regions = thickness_volume.columns                               
                               
data = demographics[['Age', 'Hand']].merge(thickness_volume, left_index=True, right_index=True)
                               
X = ['Age', 'Hand']
Y = brain_regions

residuals = thickness_volume.copy()
residuals[brain_regions] = covar_correct(X, Y, data, n_jobs=nj)


residuals.to_csv(f"{data_dir}/Data_residuals.csv")

logging.debug(f"DATA CORRECTED FOR CONFOUNDS\n{log_func(locals())}\n\n")
