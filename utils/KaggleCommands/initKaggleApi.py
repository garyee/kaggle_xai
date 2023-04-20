from kaggle.api.kaggle_api_extended import KaggleApi

api=None

def getApi():
    global api
    if api==None:
        api = KaggleApi()
        api.authenticate()
    return api