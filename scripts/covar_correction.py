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

covariate_columns = ['Age', 'Hand', 'Icv']

def covar_correct(X, Y, data, n_jobs=nj):
    
    def get_resid(X, y, data, n_jobs=n_jobs):
        r = data[y] - LinearRegression(n_jobs=n_jobs).fit(data[X], data[y]).predict(data[X])
        return r
    
    R = Parallel(n_jobs=n_jobs)(delayed(get_resid)(X, y, data, n_jobs=n_jobs) for y in Y)
    return np.asanyarray(R).T



demographics = pd.read_csv(f"{data_dir}/Demographics.csv", index_col="SubjID")
thickness_volume = pd.read_csv(f"{data_dir}/CT_Volume.csv", index_col="SubjID")
brain_regions = thickness_volume.columns                               

cortical_regions = pd.read_csv(f"{data_dir}/CorticalMeasuresENIGMA_ThickAvg.csv", index_col="SubjID").columns
cortical_regions = pd.Series(cortical_regions.str.split('_')).apply(lambda x: ''.join(str.capitalize(s) for s in x))
subcortical_structures = pd.read_csv(f"{data_dir}/SubcorticalMeasuresENIGMA_VolAvg.csv", index_col="SubjID").columns
subcortical_structures = pd.Series(subcortical_structures.str.split('_')).apply(lambda x: ''.join(str.capitalize(s) for s in x))

data = demographics[covariate_columns].merge(thickness_volume, left_index=True, right_index=True)
                               
X = ['Age', 'Hand']
Y = cortical_regions[np.isin(cortical_regions, thickness_volume.columns)]
residuals = thickness_volume.copy()
residuals[Y] = covar_correct(X, Y, data, n_jobs=nj)


X = ['Age', 'Hand', 'Icv']
Y = subcortical_structures[np.isin(subcortical_structures, thickness_volume.columns)]
residuals = thickness_volume.copy()
residuals[Y] = covar_correct(X, Y, data, n_jobs=nj)

residuals.to_csv(f"{data_dir}/Data_residuals.csv")

logging.debug(f"DATA CORRECTED FOR CONFOUNDS\n{log_func(locals())}\n\n")
