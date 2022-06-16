import pandas as pd
import numpy as np
import os

import datasets

from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.tree import SurvivalTree
from sksurv.ensemble import RandomSurvivalForest
from sksurv.ensemble import GradientBoostingSurvivalAnalysis

dict_ds = {
    "PBC": datasets.load_pbc_dataset,
    "GBSG": datasets.load_gbsg_dataset,
    "Wuhan": datasets.load_wuhan_dataset
}

dict_models = {
    "CoxPH": CoxPHSurvivalAnalysis,
    "SurvTree": SurvivalTree,
    "RSF": RandomSurvivalForest,
    "GBSA": GradientBoostingSurvivalAnalysis
}


def create_model(dataset_name="PBC", model_name="CoxPH"):
    if dataset_name in dict_ds:
        ds = dict_ds[dataset_name]()
    X, y, features, categ, sch_nan = ds
    if model_name in dict_models:
        X = X.fillna(0).replace(np.nan, 0)
        model = dict_models[model_name]()
    model.fit(X, y)
    dir_path = os.path.join(os.path.dirname(__file__), "models", dataset_name)
    model_path = os.path.join(dir_path, model_name + '.pickle')
    X_path = os.path.join(dir_path, dataset_name + '_X.csv')
    y_path = os.path.join(dir_path, dataset_name + '_y.csv')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    datasets.save_pickle(model, model_path)
    X.to_csv(X_path, index=False)
    pd.DataFrame(y).to_csv(y_path, index=False)
    return X_path, y_path, model_path