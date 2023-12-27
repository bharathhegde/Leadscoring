DB_PATH = '/home/airflow/dags/Lead_scoring_data_pipeline/'
DB_FILE_NAME = 'lead_scoring_data_cleaning.db'

DB_FILE_MLFLOW = 'Lead_scoring_mlflow_production.db'
MLFLOW_PATH = '/home/Assignment/mlruns/'

TRACKING_URI = "http://0.0.0.0:6006"
EXPERIMENT = "Lead_scoring_mlflow_production"

# model config imported from pycaret experimentation
model_config = {
            'bagging_fraction':0.887437593014418, 
            'bagging_freq':1,
            'boosting_type': 'gbdt',
            'class_weight': None,
            'colsample_bytree': 1.0,
            'feature_fraction': 0.7588282465072769,
            'importance_type': 'split' ,
            'learning_rate': 0.037577891518562063,
            'max_depth': -1,
            'min_child_samples': 53,
            'min_child_weight': 0.001,
            'min_split_gain': 0.09545503921499346,
            'n_estimators': 229,
            'n_jobs': -1,
            'num_leaves': 224,
            'objective': None,
            'random_state': 42,
            'reg_alpha': 1.074527356155175,
            'reg_lambda': 1.7978270329637185e-06,
            'silent': 'warn',
            'subsample': 1.0,
            'subsample_for_bin': 200000 ,
            'subsample_freq': 0
            }

# list of the features that needs to be there in the final encoded dataframe
ONE_HOT_ENCODED_FEATURES = ['total_leads_droppped','city_tier', 'first_platform_c_others','first_platform_c_Level8', 'first_platform_c_Level0','first_platform_c_Level2', 'first_platform_c_Level7', 'first_platform_c_Level1','first_utm_medium_c_Level0', 'first_utm_source_c_Level6', 'first_utm_medium_c_others', 'first_utm_source_c_others', 'app_complete_flag']

# list of features that need to be one-hot encoded
FEATURES_TO_ENCODE = ["first_platform_c", "first_utm_medium_c", "first_utm_source_c"]
