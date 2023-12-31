# -*- coding: utf-8 -*-
"""Nur Aula_DS_Project_1_Laptop_Price_Dataset_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MwZDWxv4rUNqNDq9CcEHkBXTa6tcA9uA

# Connect to G-Drive
"""

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

"""## Change Notebook Default Directory"""

# Change the current working directory to "/content/drive/MyDrive/Project I"
import os
file_dir = "/content/drive/MyDrive/Project I"
os.chdir(file_dir)

# List the files and directories in the current working directory
!ls

"""# Import Libraries"""

# Data Analysis Libraries
import pandas as pd
import numpy as np

# Data Viz Libraries
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid") # Seaborn theme options other than "whitegrid" are "darkgrid", "dark", "white", "ticks"
sns.despine() # Remove any spines (the outer edges of the plot) from a plot
plt.style.use("seaborn-whitegrid") # Style plot of Matplotlib
plt.rc("figure", autolayout=True) # RC = Runtime Configuration
plt.rc("axes",
       labelweight="bold",
       labelsize="large",
       titleweight="bold",
       titlesize=14,
       titlepad=10
)

# RegEx
import regex as re

"""# Load Dataset"""

# Load dataset
csv_filename = "[Complete]Laptop_Price.csv"
df = pd.read_csv(csv_filename)

df.head()

"""## DataFrame's Info"""

# DataFrame shape
df.shape

# DataFrame info
df.info()

"""Observations:

*   The DataFrame has a RangeIndex ranging from 0 to 1302 and a total of 1303 entries. It comprises 13 columns, each with a specific name and associated data.
*   Some columns, such as 'Ram', 'Memory', and 'Weight', appear to contain categorical or string data. These columns might need to be converted to numerical types if they are supposed to represent numerical values.
*   The numerical columns in the provided DataFrame snippet include 'laptop_ID,' representing unique numerical identifiers for each laptop; 'Inches,' indicating the size of the laptop screen in inches; and 'Price_euros,' representing the price of the laptop in euros.
*   The 'ScreenResolution' column might need parsing or preprocessing to extract relevant information.

In summary, this DataFrame appears to contain information about laptops, with various features such as company, product name, specifications, and pricing.

## Describe Dataframe
"""

# Describe DataFrame
df.describe()

"""Using the '**describe**' method of the dataframe, we can get some first insights on the numerical columns.

Observations:

*   The 'laptop_ID' ranges from 1 to 1320 with an average of approximately 660.16 and a standard deviation of about 381.17.
*   The 'Inches' column, representing laptop screen sizes, has a mean of approximately 15.02 inches, with a standard deviation of around 1.43 inches.
*   For 'Price_euros,' the average price is approximately 1123.69 euros, with a standard deviation of about 699.01 euros. The minimum and maximum prices are 174 euros and 6099 euros, respectively.
*   The data also includes percentiles, such as the median ('laptop_ID': 659, 'Inches': 15.6, 'Price_euros': 977), providing insights into the distribution of these numerical features.

# Data Cleaning

## Lowering DataFrame's Column Names
"""

# Lowering DataFrame's column names
df.columns = df.columns.str.lower()
df.head()

"""## Check Missing Values"""

# Check for missing values
missing_values = df.isnull().sum()
missing_values

"""## Check For Duplicates"""

# Check for duplicates
duplicates = df.duplicated().sum()
duplicates

"""# Data Cleaning + Feature Engineering (FE)

## Laptop ID Data Cleaning
"""

# Check for missing values in 'laptop_id'
missing_values_in_laptop_id = df['laptop_id'].isnull().sum()
missing_values_in_laptop_id

# Check for duplicates in 'laptop_id'
duplicates_in_laptop_id = df['laptop_id'].duplicated().sum()
duplicates_in_laptop_id

# Check data type of 'laptop_id'
data_type_of_laptop_id = df['laptop_id'].dtype
data_type_of_laptop_id

# Check unique values of 'laptop_id'
df.laptop_id.unique()

"""## Laptop ID Feature Engineering (FE)"""

# Set 'laptop_id' as the DataFrame index
df.set_index('laptop_id', inplace=True) # When inplace = True , the data is modified in place, which means it will return nothing and the dataframe is now updated

"""## Screen Resolution Data Cleaning"""

# Check for missing values in 'screenresolution'
missing_values_in_screenresolution = df['screenresolution'].isnull().sum()
missing_values_in_screenresolution

# Check for duplicates in 'screenresolution'
duplicates_in_screenresolution = df['screenresolution'].duplicated().sum()
duplicates_in_screenresolution

# Check data type of 'screenresolution'
data_type_of_screenresolution = df['screenresolution'].dtype
data_type_of_screenresolution

# Check unique values of 'screenresolution'
df.screenresolution.unique()

"""## Screen Resolution Feature Engineering (FE)"""

# Create new columns for resolution width and height
df['resolution_width'] = df['screenresolution'].str.extract(r'(\d+)x(\d+)')[0].str.strip()
df['resolution_height'] = df['screenresolution'].str.extract(r'(\d+)x(\d+)')[1].str.strip()
df.head()

# Create a new column for aspect ratio
df['aspect_ratio'] = df['resolution_width'].astype(float) / df['resolution_height'].astype(float)
df.head()

# Create a column for the resolution type and touchscreen feature

# Check if 'screenresolution' contains any alphabetic characters
df['has_alphabetic'] = df['screenresolution'].str.contains('[a-zA-Z]')

# Set 'resolution_type' based on the condition
df['resolution_type'] = np.where(df['has_alphabetic'], df['screenresolution'].str.extract(r'([a-zA-Z\s]+)')[0], 'Other')

# Create a column for the touchscreen feature
df['touchscreen'] = np.where(df['screenresolution'].str.contains('Touchscreen', case=False), 'Yes', 'No')

# For cases where 'screenresolution' doesn't contain alphabetic characters or has a numeric format like "1440x900", set 'resolutiontype' to 'Other'
df.loc[~df['has_alphabetic'] | df['screenresolution'].str.match(r'\d+x\d+'), 'resolution_type'] = 'Other'

# Drop the intermediate column 'has_alphabetic'
df = df.drop(columns=['has_alphabetic'])

df

# Dropping the original 'screenresolution' column
df = df.drop(columns=['screenresolution'])
df.head()

"""## CPU Data Cleaning"""

# Check for missing values in 'cpu'
missing_values_in_cpu = df['cpu'].isnull().sum()
missing_values_in_cpu

# Check for duplicates in 'cpu'
duplicates_in_cpu = df['cpu'].duplicated().sum()
duplicates_in_cpu

# Check data type of 'cpu'
data_type_of_cpu = df['cpu'].dtype
data_type_of_cpu

# Check unique values of 'cpu'
df.cpu.unique()

"""## CPU Feature Engineering (FE)"""

# Extract CPU manufacturer and model
df['cpu_manufacturer'] = df['cpu'].str.split(n=1).str[0]
df['cpu_model_with_clock'] = df['cpu'].str.split(n=1).str[1]

# Remove clock speed from the model
df['cpu_model'] = df['cpu_model_with_clock'].str.replace(r'\d+\.*\d*GHz', '').str.strip()

# Drop intermediate columns
df = df.drop(columns=['cpu_model_with_clock'])
df

# Extract CPU clock speed in GHz
df['cpu_clock_speed_GHz'] = df['cpu'].str.extract(r'(\d+\.*\d*)GHz').astype(float)

df.head()

# Dropping the original 'cpu' column
df = df.drop(columns=['cpu'])
df.head()

"""## RAM Data Cleaning"""

# Check for missing values in 'ram'
missing_values_in_ram = df['ram'].isnull().sum()
missing_values_in_ram

# Check for duplicates in 'ram'
duplicates_in_ram = df['ram'].duplicated().sum()
duplicates_in_ram

# Check data type of 'ram'
data_type_of_ram = df['ram'].dtype
data_type_of_ram

# Check unique values of 'ram'
df.ram.unique()

"""## RAM Feature Engineering (FE)"""

# Change the RAM data type to float
df['ram_gb'] = df['ram'].str.extract('(\d+\.*\d*)').astype(float)
df.head()

# Dropping the original 'ram' column
df = df.drop(columns=['ram'])
df.head()

"""## Memory (Drive) Data Cleaning"""

# Check for missing values in 'memory'
missing_values_in_memory = df['memory'].isnull().sum()
missing_values_in_memory

# Check for duplicates in 'memory'
duplicates_in_memory = df['memory'].duplicated().sum()
duplicates_in_memory

# Check data type of 'memory'
data_type_of_memory = df['memory'].dtype
data_type_of_memory

# Check unique values of 'memory'
df.memory.unique()

"""## Memory (Drive) Feature Engineering (FE)"""

## Remove storage capacity types from storage capacity numbers
df['memory'] = df['memory'].str.replace(r'GB|\.0', '' ,regex=True)
df['memory'] = df['memory'].str.replace(r'TB','000',regex=True)
df['memory'].unique()

# Set 'storage_capacity1' and 'storage_capacity2' columns
df['storage_capacity1']= df['memory'].str.replace(r' ','').str.split('+', n = 1, expand = True)[0]
df['storage_capacity2']=df['memory'].str.replace(r' ','').str.split('+', n = 1, expand = True)[1]
print('storage_capacity1 Values: ',df['storage_capacity1'].unique())
print('storage_capacity2 Values: ',df['storage_capacity2'].unique())

# Set 'storage_type1' and 'storage_type2' columns
df['storage_type1'] = df['storage_capacity1'].str.extract(r'(\D+)')
df['storage_type2'] = df['storage_capacity2'].str.extract(r'(\D+)')

# Remove storage types from 2 storage capacity columns
df['storage_capacity1'] = df['storage_capacity1'].str.extract(r'(\d+)',)
df['storage_capacity2'] = df['storage_capacity2'].str.extract(r'(\d+)',)

# Convert storage capacity columns data type
df['storage_capacity1'] = df['storage_capacity1'].astype('float64')
df['storage_capacity2'] = df['storage_capacity2'].astype('float64')

# Handling missing values
df['storage_capacity2'] = df['storage_capacity2'].fillna('0')
df['storage_type2'] = df['storage_type2'].fillna('None')

df.head()

# Dropping the original 'memory' column
df = df.drop(columns=['memory'])
df.head()

"""## Weight Data Cleaning

"""

# Check for missing values in 'weight'
missing_values_in_weight = df['weight'].isnull().sum()
missing_values_in_weight

# Check for duplicates in 'weight'
duplicates_in_weight = df['weight'].duplicated().sum()
duplicates_in_weight

# Check data type of 'weight'
data_type_of_weight = df['weight'].dtype
data_type_of_weight

# Check unique values of 'weight'
df.weight.unique()

"""## Weight Feature Engineering (FE)

"""

# Create a new column 'weight_kg' and convert it to float type
df['weight_kg'] = df['weight'].str.extract(r'(\d+\.*\d*)\s*(kg)')[0]
df['weight_kg'] = df['weight_kg'].astype('float')

df.head()

# Check data type of 'weight_kg'
data_type_of_weight_kg = df['weight_kg'].dtype
data_type_of_weight_kg

# Dropping the original 'weight' column
df = df.drop(columns=['weight'])
df.head()

"""## GPU Data Cleaning"""

# Check for missing values in 'gpu'
missing_values_in_gpu = df['gpu'].isnull().sum()
missing_values_in_gpu

# Check for duplicates in 'gpu'
duplicates_in_gpu = df['gpu'].duplicated().sum()
duplicates_in_gpu

# Check data type of 'gpu'
data_type_of_gpu = df['gpu'].dtype
data_type_of_gpu

# Check unique values of 'gpu'
df.gpu.unique()

"""## GPU Feature Engineering (FE)"""

# Create a new column 'gpu_brand'
df['gpu_brand'] = df['gpu'].str.extract(r'([a-zA-Z\s]+)((\d+\.*\d*)\s*)')[0]

# Create a new column 'gpu_model' and convert it to integer data type
df['gpu_model'] = df['gpu'].str.extract(r'([a-zA-Z\s]+)((\d+\.*\d*)\s*)')[1]
df['gpu_model'] = df['gpu_model'].astype('Int64')

df.head()

# Check data type of 'gpu_model'
data_type_of_gpu_model = df['gpu_model'].dtype
data_type_of_gpu_model

# Dropping the original 'gpu' column
df = df.drop(columns=['gpu'])
df.head()

"""Now the dataset looks clean and ready to be explored"""

df.to_csv('/content/drive/MyDrive/Colab Notebooks/[Cleaned]Laptop_Price.csv', index=False)

"""# Exploratory Data Analysis (EDA)

## Load Cleaned Dataset
"""

# Load cleaned dataset
csv_cleanfilename = "/content/drive/MyDrive/Colab Notebooks/[Cleaned]Laptop_Price.csv"
df_cleaned = pd.read_csv(csv_cleanfilename)

df_cleaned.head()

# Cleaned DataFrame shape
df_cleaned.shape

# Cleaned DataFrame info
df_cleaned.info()

# Describe cleaned DataFrame
df_cleaned.describe()

"""## Custom functions to improve plot readability"""

def num_plot(df_cleaned, col, title, symb):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(8,5),gridspec_kw={"height_ratios": (.2, .8)})
    ax[0].set_title(title,fontsize=18)
    sns.boxplot(x=col, data=df_cleaned, ax=ax[0])
    ax[0].set(yticks=[])
    sns.histplot(x=col, data=df_cleaned, ax=ax[1])
    ax[1].set_xlabel(col, fontsize=16)
    plt.axvline(df_cleaned[col].mean(), color='#DD4470', linewidth=2.2, label='mean=' + str(np.round(df_cleaned[col].mean(),1)) + symb)
    plt.axvline(df_cleaned[col].median(), color='#C6DF76', linewidth=2.2, label='median='+ str(np.round(df_cleaned[col].median(),1)) + symb)
    plt.axvline(df_cleaned[col].mode()[0], color='#FFE3B3', linewidth=2.2, label='mode='+ str(df_cleaned[col].mode()[0]) + symb)
    plt.legend(bbox_to_anchor=(1, 1.03), ncol=1, fontsize=17, fancybox=True, shadow=True, frameon=True)
    plt.tight_layout()
    plt.show()

num_plot(df_cleaned, 'inches', 'Screen Size Analysis', ' inches')

# Combine into total pixels
df_cleaned['total_pixels'] = df_cleaned['resolution_width'] * df_cleaned['resolution_height']

# Combined Visualization
num_plot(df_cleaned, 'total_pixels', 'Total Resolution Analysis', ' px')

num_plot(df_cleaned, 'aspect_ratio', 'Aspect Ratio Analysis', '')

"""## Which brand is the most frequent in the dataframe?"""

# Most frequent brand in cleaned DataFrame
brand_counts = df_cleaned['company'].value_counts()
brand_counts

"""So, the most frequent brands are Dell and Lenovo

## What type of laptop is the most frequent?
"""

# Most frequent type of laptop in cleaned DataFrame
most_frequent_type = df_cleaned['typename'].value_counts().idxmax()
print(f"The most frequent type of laptop is: {most_frequent_type}")

"""## Which size is the most popular?"""

# Most popular size in cleaned DataFrame
most_popular_size = df_cleaned['inches'].value_counts().idxmax()
print(f"The most popular size is: {most_popular_size} inches")

"""## How is weight distributed among the laptops?"""

def plot_weight_distribution(df_cleaned):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_cleaned['weight_kg'], bins=50, kde=True, color='pink')
    plt.title('Distribution of Laptop Weights')
    plt.xlabel('Weight (kg)')
    plt.ylabel('Frequency')
    plt.show()

plot_weight_distribution(df_cleaned)

"""## How is price distributed among the laptops?"""

num_plot(df_cleaned, 'price_euros', 'Price Analysis', ' euros')

"""## How is RAM distributed among the laptops?"""

num_plot(df_cleaned, 'ram_gb', 'RAM Analysis', ' GB')

"""## How is CPU frequency distributed among the laptops?"""

num_plot(df_cleaned, 'cpu_clock_speed_GHz', 'CPU Clock Speed Analysis', ' GHz')

"""## How is Hard Drive capacity distributed among the laptops?"""

num_plot(df_cleaned, 'storage_capacity1', 'Hard Drive Primary Capacity Distribution Analysis', ' GB')

num_plot(df_cleaned, 'storage_capacity2', 'Hard Drive Secondary Capacity Distribution Analysis', ' GB')

"""## Price VS CPU brand by GPU brand"""

# Scatter plot: Price vs. CPU brand, colored by GPU brand
plt.figure(figsize=(12, 8))
sns.scatterplot(x='cpu_manufacturer', y='price_euros', hue='gpu_brand', data=df_cleaned, palette='viridis', alpha=0.7)
plt.title('Price vs. CPU brand by GPU brand')
plt.xlabel('CPU Manufacturer')
plt.ylabel('Price (Euros)')
plt.show()

"""Insights from this plot:

* Laptops with Intel processors are more prevalent in the dataset
* AMD CPUs are also well-represented but perhaps not as dominant as Intel
* Samsung may not be as prevalent in the laptop market compared to Intel and AMD

## Which are the TOP 15 most common GPUs?
"""

top_gpus = df_cleaned['gpu_model'].value_counts().head(15)

plt.figure(figsize=(12, 6))
top_gpus.plot(kind='bar', color='skyblue')
plt.title('Top 15 Most Common GPUs')
plt.xlabel('GPU Model')
plt.ylabel('Count')
plt.show()

"""## Which are the TOP 15 most common CPUs?"""

top_cpus = df_cleaned['cpu_model'].value_counts().head(15)

plt.figure(figsize=(12, 6))
top_cpus.plot(kind='bar', color='skyblue')
plt.title('Top 15 Most Common CPUs')
plt.xlabel('CPU Model')
plt.ylabel('Count')
plt.show()

"""## What is the average price of laptops by company?"""

# Group the data by the 'company' column and then calculate the mean price for each group
average_price_by_company = df_cleaned.groupby('company')['price_euros'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
average_price_by_company.plot(kind='bar', color='lightblue')
plt.title('Average Price of Laptops by Company')
plt.xlabel('Company')
plt.ylabel('Average Price (Euros)')
plt.show()

"""Insights:
* Razer has the highest average price
* Dell, Lenovo, and Asus are mid-range
* Brands with higher average prices may be perceived as premium, while those with lower average prices may be targetting budget-conscious customers
"""