import os
import pickle
import scipy
import numpy

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from zenml.steps import step, Output
from zenml.pipelines import pipeline

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

@step
def importer() -> Output(
    X_train=scipy.sparse.csr.csr_matrix,
    X_test=scipy.sparse.csr.csr_matrix,
    y_train=numpy.ndarray,
    y_test=numpy.ndarray,
):
    X_train, y_train = load_pickle(os.path.join("./output", "train.pkl"))
    X_val, y_val = load_pickle(os.path.join("./output", "val.pkl"))
    return X_train, X_val, y_train, y_val

@step
def trainer(X_train: scipy.sparse.csr.csr_matrix, y_train: numpy.ndarray) -> RandomForestRegressor:
    rf = RandomForestRegressor(max_depth=10, random_state=0)
    rf.fit(X_train, y_train)
    return rf

@step
def evaluator(X_test: scipy.sparse.csr.csr_matrix, y_test: numpy.ndarray, model: RandomForestRegressor) -> numpy.float64:
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"RMSE: {rmse}")   
    return rmse

@pipeline
def pipeline(importer, trainer, evaluator):
    X_train, X_test, y_train, y_test = importer()
    model = trainer(X_train=X_train, y_train=y_train)
    evaluator(X_test=X_test, y_test=y_test, model=model)

if __name__ == '__main__':
    # todo enable logging to terminal
    print(pipeline(
        importer=importer(), trainer=trainer(), evaluator=evaluator()
    ).run(unlisted=False))