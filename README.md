# Bike Rental Performance in 2011 - 2012 🚲
This repository contains the codebase for "Bike Rental Performance in 2011 - 2012 App". The training notebooks & the datasets are also provided in the respective folders.

## Setup Environment - Google Colab Notebook
Dashboard_Proyek_DA.py is the streamlit app code. run the command "pip install -r requirements.txt" to install the required dependencies for the streamlit app.
You may need to install additional libraries for running the jupyter notebooks.
```
pip install -r requirements.txt
```
## Run Streamlit App - Google Colab Notebook
Create new notebook and running this code below
```
pip install streamlit -q
!wget -q -O - ipv4.icanhazip.com
! streamlit run '/content/drive/MyDrive/dashboard/Dashboard_Proyek_DA.py' & npx localtunnel --port 8501
```
