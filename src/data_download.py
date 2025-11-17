
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

#download movie dataset
kaggle.api.dataset_download_files('manchunhui/uk-hospitals', path= ',', unzip=True)