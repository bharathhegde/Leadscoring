'''
filename: utils.py
functions: encode_features, get_train_model
creator: shashank.gupta
version: 1
'''

###############################################################################
# Import necessary modules
# ##############################################################################

import pandas as pd
import numpy as np

import sqlite3
from sqlite3 import Error

import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
    auc
)
from sklearn.metrics import precision_recall_fscore_support


from Lead_scoring_training_pipeline.constants import *
from datetime import date

import contextlib
import logging


###############################################################################
# Define the function to encode features
# ##############################################################################

def encode_features():
    '''
    This function one hot encodes the categorical features present in our  
    training dataset. This encoding is needed for feeding categorical data 
    to many scikit-learn models.

    INPUTS
        db_file_name : Name of the database file 
        db_path : path where the db file should be
        ONE_HOT_ENCODED_FEATURES : list of the features that needs to be there in the final encoded dataframe
        FEATURES_TO_ENCODE: list of features  from cleaned data that need to be one-hot encoded
       

    OUTPUT
        1. Save the encoded features in a table - features
        2. Save the target variable in a separate table - target


    SAMPLE USAGE
        encode_features()
        
    **NOTE : You can modify the encode_featues function used in heart disease's inference
        pipeline from the pre-requisite module for this.
    '''
    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    
    print("Loading model_input")
    df = pd.read_sql("select * from model_input", conn)
    
    print("One hot encoding features")
    encoded_df = pd.DataFrame(columns= ONE_HOT_ENCODED_FEATURES) # from constants.py
    placeholder_df = pd.DataFrame()
    
    # One-Hot Encoding using get_dummies for the specified categorical features
    for f in FEATURES_TO_ENCODE:
        if(f in df.columns):
            encoded = pd.get_dummies(df[f])
            encoded = encoded.add_prefix(f + '_')
            placeholder_df = pd.concat([placeholder_df, encoded], axis=1)
        else:
            print('Feature not found')
            return df
    
    # Implement these steps to prevent dimension mismatch during inference
    for feature in encoded_df.columns:
        if feature in df.columns:
            encoded_df[feature] = df[feature]
        if feature in placeholder_df.columns:
            encoded_df[feature] = placeholder_df[feature]
    # fill all null values
    encoded_df.fillna(0, inplace=True)
    
    #Splitting X,y 
    features = encoded_df.drop('app_complete_flag',axis=1)
    target = encoded_df[['app_complete_flag']]
    
    print("Storing 'target' table")
    target.to_sql(name="target", con=conn, if_exists="replace", index=False)
    print("Storing feature table")
    features.to_sql(name="features", con=conn, if_exists="replace", index=False)
    
    conn.close()


###############################################################################
# Define the function to train the model
# ##############################################################################

def get_trained_model():
    '''
    This function setups mlflow experiment to track the run of the training pipeline. It 
    also trains the model based on the features created in the previous function and 
    logs the train model into mlflow model registry for prediction. The input dataset is split
    into train and test data and the auc score calculated on the test data and
    recorded as a metric in mlflow run.   

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be


    OUTPUT
        Tracks the run in experiment named 'Lead_Scoring_Training_Pipeline'
        Logs the trained model into mlflow model registry with name 'LightGBM'
        Logs the metrics and parameters into mlflow run
        Calculate auc from the test data and log into mlflow run  

    SAMPLE USAGE
        get_trained_model()
    '''
    
    conn = None
    # opening the connection for sqlite db for mlflow
    try:
        conn = sqlite3.connect(MLFLOW_PATH + DB_FILE_MLFLOW)
        print(sqlite3.version)
    # return an error if connection not established
    except Error as e:
        print(e)
    # closing the connection once the database is created
    finally:
        if conn:
            conn.close()
    
    cnx = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    X = pd.read_sql('select * from features', cnx)
    y = pd.read_sql('select * from target', cnx)
    cnx.close()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
    
    mlflow.set_tracking_uri(TRACKING_URI)
    run_name = EXPERIMENT + "" + date.today().strftime("%d%m_%Y_%H_%M_%S")
    
    with contextlib.suppress(Exception):
        # Creating an experiment
        logging.info("Creating a mlflow experiment")
        mlflow.create_experiment(EXPERIMENT)
        # Setting the environment with the created experiment
        mlflow.set_experiment(EXPERIMENT)

        #Model Training

    with mlflow.start_run(run_name=run_name) as run:
        #Model Training
        clf = lgb.LGBMClassifier()
        clf.set_params(**model_config) 
        clf.fit(X_train, y_train)

        mlflow.sklearn.log_model(sk_model=clf,artifact_path="models", registered_model_name='LightGBM')
        mlflow.log_params(model_config)    

        # predict the results on training dataset
        y_pred=clf.predict(X_test)

        #Log metrics
        acc=accuracy_score(y_pred, y_test)
        conf_mat = confusion_matrix(y_pred, y_test)
        precision = precision_score(y_pred, y_test,average= 'macro')
        recall = recall_score(y_pred, y_test, average= 'macro')
        f1 = f1_score(y_pred, y_test, average='macro')
        cm = confusion_matrix(y_test, y_pred)
        auc = roc_auc_score(y_pred, y_test, average="weighted", multi_class="ovr")

        tn = cm[0][0]
        fn = cm[1][0]
        tp = cm[1][1]
        fp = cm[0][1]
        class_zero = precision_recall_fscore_support(y_test, y_pred, average='binary',pos_label=0)
        class_one = precision_recall_fscore_support(y_test, y_pred, average='binary',pos_label=1)
        
        print("Recall=", recall)
        print("Precision=", precision)
        print("AUC=", auc)

        mlflow.log_metric('auc', auc)
        mlflow.log_metric('test_accuracy', acc)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("Precision", precision)
        mlflow.log_metric("Recall", recall)
        mlflow.log_metric("Precision_0", class_zero[0])
        mlflow.log_metric("Precision_1", class_one[0])
        mlflow.log_metric("Recall_0", class_zero[1])
        mlflow.log_metric("Recall_1", class_one[1])
        mlflow.log_metric("f1_0", class_zero[2])
        mlflow.log_metric("f1_1", class_one[2])
        mlflow.log_metric("False Negative", fn)
        mlflow.log_metric("True Negative", tn)

        runID = run.info.run_uuid
        print("Inside MLflow Run with id {}".format(runID))


   
