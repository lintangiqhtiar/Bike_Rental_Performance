# Bike Rental Performance in 2011 - 2012 🚲
This repository contains the codebase for "Bike Rental Performance in 2011 - 2012 App". The training notebooks & the datasets are also provided in the respective folders.

## Setup Environment - Google Colab Notebook
Dashboard_Proyek_DA.py is the streamlit app code. Create new notebook and run the command below to install the required dependencies for the streamlit app.
You may need to install additional libraries for running the notebook.
```
pip install -r requirements.txt
```
## Run Streamlit App - Google Colab Notebook
Add the command below to run the Streamlit App
```
pip install streamlit -q
!wget -q -O - ipv4.icanhazip.com
! streamlit run '/content/drive/MyDrive/dashboard/Dashboard_Proyek_DA.py' & npx localtunnel --port 8501
```
