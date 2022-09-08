1. install the dependencies listed in the setup.sh
2. create a file with a Kaggle access token, for details see https://github.com/Kaggle/kaggle-api#api-credentials
3. configure the following variables:
 file utils/KaggleEnums.py - line 50 - filePath set it to your local path
4. launch the main.py to start the process of filling the database

I allways launched the downloader on Colab, the notebook file is in the /Downloaders folder. It downloads the notbooks into google drive (path has to be configured). I installed the desktop app and synced them to my local drive. That way I did not expirience many download restrictions and I could launch the script from everywhere.