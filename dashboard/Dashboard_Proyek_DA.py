
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

file_path_day = "dashboard/cleaned_df_day.csv"
df_day = pd.read_csv(file_path_day)
file_path_hour = "dashboard/cleaned_df_hour.csv"
df_hour = pd.read_csv(file_path_hour)

def create_performance_df(df):
   # Mengelompokkan data berdasarkan 'dteday' dan menjumlahkan 'cnt'
    performance_df = df.groupby('dteday')['cnt'].sum().reset_index()
    
    # Memberi nama kolom yang sesuai
    performance_df.columns = ['dteday', 'cnt']
    
    return performance_df

def create_performance_daily_df(df):
  performance_inaweek = df.groupby('weekday')[['casual', 'registered', 'cnt']].sum()
  performance_inaweek = performance_inaweek.reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
  performance_inaweek = performance_inaweek.reset_index()
  return performance_inaweek

def create_performance_hourly_df(df):
  performance_hourly = df.groupby('hr')[['casual', 'registered', 'cnt']].sum()
  performance_hourly = performance_hourly.reindex(range(0, 24))
  performance_hourly=performance_hourly.reset_index()
  return performance_hourly

def create_rent_amount_daily_by_season_df(df):
  rent_amount_daily = df.groupby(['season', 'weathersit'])[['casual', 'registered', 'cnt']].sum()
  rent_amount_daily = rent_amount_daily.reset_index()
  return rent_amount_daily

def create_rent_amount_hourly_by_season_df(df):
  rent_amount_hourly = df.groupby(['season', 'weathersit'])[['casual', 'registered', 'cnt']].sum()
  rent_amount_hourly = rent_amount_hourly.reset_index()
  return rent_amount_hourly

def create_performance_rent_amount_by_environmental_variables(df):
  performance_by_condition = df.groupby('dteday').agg({
      'temp_in _celcius': 'mean',
      'atemp_in _celcius': 'mean',
      'humidity': 'mean',
      'windspeed_value': 'mean',
      'casual': 'sum',
      'registered': 'sum',
      'cnt': 'sum'
  }).sort_values('dteday', ascending=False)

  #reset index menjadi per bulan
  performance_by_condition = performance_by_condition.reset_index()
  performance_by_condition['dteday'] = pd.to_datetime(performance_by_condition['dteday'])
  performance_by_condition['month'] = performance_by_condition['dteday'].dt.month
  performance_by_condition = performance_by_condition.groupby('month').mean()
  performance_by_condition = performance_by_condition.reset_index()
  
  month_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
  }

  performance_by_condition['month'] = performance_by_condition['month'].map(month_dict)
  return performance_by_condition

#membuat kolom datetime
datetime_column = ['dteday']
df_day.sort_values(by='dteday', inplace=True)
df_day.reset_index(inplace= True)

for column in datetime_column :
  df_day[column] = pd.to_datetime(df_day[column])

min_date = df_day['dteday'].min()
max_date = df_day['dteday'].max()

st.header('Bike Rental Performance at 2011 - 2012')
#input tanggal
start_date, end_date = st.date_input(
  label='Rentang waktu',
  min_value=min_date,
  max_value=max_date,
  value=[min_date, max_date]
)

main_df_day = df_day[(df_day['dteday']>= str(start_date)) & (df_day['dteday']<= str(end_date))]

# Mengurutkan data berdasarkan kolom 'hr'
df_hour.sort_values(by='hr', inplace=True)
df_hour.reset_index(drop=True, inplace=True)

# Tidak perlu konversi ke timedelta jika kolom 'hr' sudah berupa angka (0-23)
# Asumsikan kolom 'hr' adalah integer yang mewakili jam dalam format 0-23

min_hour = df_hour['hr'].min()
max_hour = df_hour['hr'].max()

# Menggunakan time_input untuk mendapatkan jam mulai dan akhir dalam rentang waktu
start_hour = st.time_input(
    label='Jam Mulai',
    value=pd.to_datetime(f'{min_hour}:00').time(),
    key='start_hour'
)

end_hour = st.time_input(
    label='Jam Akhir',
    value=pd.to_datetime(f'{max_hour}:00').time(),
    key='end_hour'
)

# Konversi waktu input ke format 24 jam (integer) untuk menyaring data
start_hour_int = start_hour.hour
end_hour_int = end_hour.hour

# Saring data berdasarkan jam yang dipilih
main_df_hour = df_hour[(df_hour['hr'] >= start_hour_int) & (df_hour['hr'] <= end_hour_int)]

performance_df = create_performance_df(main_df_day)
performance_inaweek = create_performance_daily_df(main_df_day)
performance_hourly = create_performance_hourly_df(main_df_hour)
rent_amount_daily = create_rent_amount_daily_by_season_df(main_df_day)
rent_amount_hourly = create_rent_amount_hourly_by_season_df(main_df_hour)
performance_by_condition = create_performance_rent_amount_by_environmental_variables(main_df_day)

#st.write(performance_df.dtypes)
st.subheader ('Daily Bike Rental Performance')

fig,ax = plt.subplots(figsize=(16,8))
ax.plot(
  performance_df["dteday"],
  performance_df["cnt"],
  marker='o', 
  linewidth=2,
  color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
  st.subheader('Rental Performance In A Week')
  fig, ax = plt.subplots(figsize=(30,15))

  ax.plot(
    performance_inaweek['weekday'],
    performance_inaweek['cnt'],
    marker='o', 
    linewidth=5,
    color="#90CAF9"
  )
  ax.set_title('Bike Rental Performance In a Week')
  ax.set_xlabel('Weekday')
  ax.set_ylabel('Rental Count')

  ax.tick_params(axis='y', labelsize=35)
  ax.tick_params(axis='x', labelsize=35)
  
  st.pyplot(fig)

with col2:
  st.subheader('Hourly Bike Rental Performance')
  fig, ax = plt.subplots(figsize=(30,15))
  ax.plot(
    performance_hourly['hr'],
    performance_hourly['cnt'],
    marker='o',
    linewidth=5,
    color= '#90CAF9'
  )
  ax.set_title('Hourly Bike Rental Performance')
  ax.set_xlabel('Weekday')
  ax.set_ylabel('Rental Count')

  ax.tick_params(axis='y', labelsize=35)
  ax.tick_params(axis='x', labelsize=35)
  
  st.pyplot(fig)

st.subheader('Rental Amount by Condition and Season')

# Membuat figure dan axis dengan ukuran yang benar
fig, ax = plt.subplots(figsize=(20, 10))

# Membuat barplot
sns.barplot(
    x='season', 
    y='cnt', 
    hue='weathersit', 
    data=rent_amount_daily
)

# Mengatur judul, label, dan ukuran font
ax.set_title("Daily Rent Amount", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

# Menampilkan plot di Streamlit
st.pyplot(fig)

#rent amount hourly

# Membuat figure dan axis dengan ukuran yang benar
fig, ax = plt.subplots(figsize=(20, 10))

# Membuat barplot
sns.barplot(
    x='season', 
    y='cnt', 
    hue='weathersit', 
    data=rent_amount_hourly
)

# Mengatur judul, label, dan ukuran font
ax.set_title("Hourly Rent Amount", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

# Menampilkan plot di Streamlit
st.pyplot(fig)

st.subheader('Bike Rental Performance by Environmental Conditions')

fig,ax = plt.subplots(figsize=(20,10))

ax.plot(
  performance_by_condition['month'],
  performance_by_condition['cnt'],
  marker='o',
  label='Total'
)

ax.set_title('Bike Rental Performance by Environmental Conditions', fontsize = 20)
ax.set_xlabel('Month')
ax.set_ylabel('Rental Amount')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig)

st.caption('Dicoding University-Lintang Iqhtiar')
