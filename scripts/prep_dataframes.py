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

	
# Assemble dataframe for analyses and screen subjects

demographics = pd.read_csv(covariates, index_col="SubjID")
dashless_columns = pd.Series(demographics.columns.str.split('_')).apply(lambda x: ''.join(str.capitalize(s) for s in x))
demographics.rename(columns=dict(zip(demographics.columns, dashless_columns)), inplace=True)

if not (demographics[["Age", "Hand"]].notna().sum() > 1).all():
    raise ValueError("The dataset seems to contain less than 2 subjects with non-missing values for Age and Handedness."
                     + "\nThe these variables are used to controll for possible confounding effects in the analyses,"
                     + "and only participants for whom this data is available are included."
                     + " Fewer than 2 such subjects would make the analyses impossible to perform.")

demographics.loc[demographics.Subtype.isna(), 'Subtype'] = 0
demographics['Minor'] = np.int32(demographics.Age<18.)
demographics['Durill3'] = np.int32(demographics.Durill<3.)
demographics['Age2'] = demographics['Age']**2

thickness_volume = pd.read_csv(thickness, index_col="SubjID", usecols=lambda x: x!='ICV').merge(pd.read_csv(volume, index_col="SubjID"), left_index=True, right_index=True)
dashless_columns = pd.Series(thickness_volume.columns.str.split('_')).apply(lambda x: ''.join(str.capitalize(s) for s in x))
thickness_volume.rename(columns=dict(zip(thickness_volume.columns, dashless_columns)), inplace=True)

macroscale_indices = ['Lthickness', 'Rthickness', 'Lsurfarea', 'Rsurfarea', 'Icv']
demographics = demographics.merge(thickness_volume[macroscale_indices], left_index=True, right_index=True)
thickness_volume = thickness_volume.drop(macroscale_indices, axis=1)


covar_regressors = ['Age', 'Hand']
to_keep = np.all(~demographics[covar_regressors].isna(), axis=1)
demographics = demographics.loc[to_keep, :]
thickness_volume = thickness_volume.loc[to_keep, :]

demographics.to_csv(f"{data_dir}/Demographics.csv")
thickness_volume.to_csv(f"{data_dir}/CT_Volume.csv")

logging.debug(f"DATAFRAME CREATED\n{log_func(locals())}\n\n")


