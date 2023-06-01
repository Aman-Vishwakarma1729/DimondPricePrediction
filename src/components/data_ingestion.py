import os
import sys
from src.logger import logging
from src.exception import CustomException

import pandas as pd
from sklearn.model_selection import train_test_split

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('artifact','train.csv')
    test_data_path  = os.path.join('artifact','test.csv')
    raw_data_path   = os.path.join('artifact','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initialize_data_ingestion(self):
        logging.info('Data ingestion method starts')

        try:
            df = pd.read_csv(os.path.join('notebooks/data','gemstone.csv'))
            logging.info('Dataset read as pandas DataFrame')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info('raw data is created')

            train_set,test_set = train_test_split(df,test_size=0.30,random_state=42)
            logging.info('Data is splitted in to train set and test set')

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            logging.info('train data is created')

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info('test data is created')

            logging.info('Ingestion of data is done')

            return(
                
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )

            

        except Exception as e:
            logging.info('Exception occured at data ingestion stage')
            raise CustomException(e,sys)