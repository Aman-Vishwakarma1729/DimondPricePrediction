import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj
from dataclasses import dataclass
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

@dataclass

class DataTransforamtionConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransforamtionConfig()
        

    def get_data_transformation_objects(self):
        

        try:
            logging.info('Data transforamtion has been initiated')

            cat_columns = ['cut','color','clarity']
            num_columns = ['carat','depth','table','x','y','z']

            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info('Data transformation pipeline initiated')

            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoding',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                    ('scaler',StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ('num_pipeline',num_pipeline,num_columns),
                ('cat_pipeline',cat_pipeline,cat_columns)
            ])
             
            logging.info('Data transformation completed')

            return preprocessor
            


        except Exception as e:
            logging.info('Exception occured during getting data transforamtion objects')
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_data_path,test_data_path):

        try:
            train_df = pd.read_csv(train_data_path)
            test_df  = pd.read_csv(test_data_path)

            logging.info('Read train and test dataset completed')
            logging.info(f'Train Dataframe Head \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head \n{test_df.head().to_string()}')

            preprocessing_obj = self.get_data_transformation_objects()

            target_column = 'price'
            drop_column = [target_column,'id']

            input_feature_training_df = train_df.drop(drop_column,axis=1)
            target_feature_training_df = train_df[target_column]
            logging.info('Training data is divided in dependent and independent data')

            input_feature_testing_df = test_df.drop(drop_column,axis=1)
            target_feature_testing_df = test_df[target_column]
            logging.info('Testing data is divided in dependent and independet data')

            input_feature_train_array = preprocessing_obj.fit_transform(input_feature_training_df)
            input_feature_test_array = preprocessing_obj.transform(input_feature_testing_df)
            logging.info('Data transformation for train and test is completed')

            train_array = np.c_[input_feature_train_array,np.array(target_feature_training_df)]
            test_array = np.c_[input_feature_test_array,np.array(target_feature_testing_df)]
            logging.info('Data transformation is done and we finally have our train and test dataset')
            
            save_obj(
                file_path = self.data_tranformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                
                    train_array,
                    test_array,
                    self.data_tranformation_config.preprocessor_obj_file_path   

            )




        except Exception as e:
            logging.info('Exception occured while initilaizing data tranforamtion')
            raise CustomException(e,sys)
    