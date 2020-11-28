#!/usr/bin/env python
# coding: utf-8

# # Galopp-Preprocessor
#
# For this step in the project I will use jupyter notebook, because it is way faster to visualize and more flexible on doin data preprocessing. (The exploratory data analysis part will also be with jupyter notebook)

# In[ ]:


print("Preprocessing...")


# ### Imports

# In[1]:


import pandas as pd
import numpy as np


# ### Load dataset

# In[2]:


galopp = pd.read_csv("csvs/all_races.csv")
galopp.sample(5)


# ### Look at general information

# In[3]:


galopp.columns


# In[4]:


print(galopp.isna().sum())
print("")
print(galopp.isna().sum()/len(galopp)*100)


# In[5]:


galopp.info()


# First thing I see is that there are some NaN values. 15 each on _Date_ and _Location_ (which are only 0.16% of the whole set). Because only a few are missing, and they are not really important to my goal, I fill them with the mode (normally not really applicable for the _Date_ , but it should be sufficient).
#
# Also, the columns 'Category' and 'Class' are missing 3115 and 4245, which are ~33% and ~46%. Normally, because they are categorical, they could be filled with the mode, but so many values are missing, so I decide to drop them, as they are not important for my goal.
#
# Next, the datatypes should be changed for _Distance_ and _Prize_ to int. But before that, the 'm' in _Distance_ and the '€' in _Prize_ have to be removed. (Also, there are '\xa0's in both columns for each entry! These have to be removed too before converting to int.). And, at last, fill the empty strings with a 0, otherwise this would lead to ValueErrors when converting to int.
#
# The _Ground_state_ always contains the prefix 'Boden: ', this can also be removed.

# In[6]:


# Drop columns
galopp.drop(columns=["Category", "Class"], inplace=True)

# Fill dates and location by
galopp["Date"].fillna(galopp["Date"].mode(), inplace=True)
galopp["Location"].fillna(galopp["Location"].mode(), inplace=True)

# Remove units
galopp["Distance"] = galopp["Distance"].apply(lambda x: x.replace("m", ""))
galopp["Prize"] = galopp["Prize"].apply(lambda x: x.replace("€", ""))

# Remove bytes
galopp["Distance"] = galopp["Distance"].apply(lambda x: x.replace("\xa0", ""))
galopp["Prize"] = galopp["Prize"].apply(lambda x: x.replace("\xa0", ""))

# Fill empty strings with 0
galopp["Distance"] = galopp["Distance"].apply(lambda x: "0" if len(x) == 0 else x)
galopp["Prize"] = galopp["Prize"].apply(lambda x: "0" if len(x) == 0 else x)

# Change datatype to int
galopp["Distance"] = galopp["Distance"].astype(int)
galopp["Prize"] = galopp["Prize"].astype(int)

# Remove 'Boden: ' prefix
galopp["Ground_state"] = galopp["Ground_state"].apply(lambda x: x.replace("Boden: ", ""))


# Looking at the dataframe again:

# In[7]:


galopp.info()


# In[8]:


galopp.sample(10)


# No NaNs and the fitting datatype, also the samples looking good aswell.
# So for those columns everything that needs to be done is done. Lets go on with the horses per race. For this, I intend to:
# - get the list of horses and make another dataframe of it
# - Clean this dataset (No column names and datatypes here)
# - Return the cleaned dataframe as a list and replace it
# - Save each horse participation in another dataframe / csv

# ### Clean races and generate a participants dataframe

# In[9]:


def clean_placement_string(x):

    if "NS" in x: # Treat "Nichtstarter", horses who didn't start the race
        x = -1
    else:
        x = x.replace(".","")
        x = x.replace("'","")
        x = x.replace("[","")
        x = x.replace("]", "")
        x = x.strip()

    return x

def clean_horse_name_string(x):
    x = x.replace("'", "")
    x = x.strip()
    x = x.lower()
    return x

def clean_jockey_name_string(x):
    x = x.replace("'", "")
    x = x.strip()
    x = x.lower()

    if "." in x:
        while "." in x:
            x = x[x.index(".", )+1:] # Get surname by dot
    elif len(x.split()) == 2:
        x = x.split()[1]  # Get surname when both names are in the name string
    else:
        pass

    return x

def clean_trainer_name_string(x):
    x = x.replace("'", "")
    x = x.strip()
    x = x.lower()

    if "." in x:
        while "." in x:
            x = x[x.index(".", )+1:] # Get surname by dot
    elif len(x.split()) == 2:
        x = x.split()[1]  # Get surname when both names are in the name string
    else:
        x=x

    return x

def clean_weight_string(x):
    x = x.replace("'", "")
    x = x.replace(",",".")
    x = x.replace("]", "")
    x = x.strip()
    return x


# In[10]:


# Load, clean, and replace each race
races = []
horses = []
columns = ["Place", "Horse_name", "Jockey_name", "Trainer_name", "Weight"]

for row in galopp["Horses"]:

    # Load row as a seperate dataset and make it a dataframe for easier editing
    split = row.split(", ")
    try:
        row_reshaped = np.array(split).reshape((-1, 5))
        race_df = pd.DataFrame(data=row_reshaped, columns=columns)

        # Clean dataset (and save a version with the races)
        race_df["Place"] = race_df["Place"].apply(clean_placement_string)
        race_df["Horse_name"] = race_df["Horse_name"].apply(clean_horse_name_string)
        race_df["Jockey_name"] = race_df["Jockey_name"].apply(clean_jockey_name_string)
        race_df["Trainer_name"] = race_df["Trainer_name"].apply(clean_trainer_name_string)
        race_df["Weight"] = race_df["Weight"].apply(clean_weight_string)

        # Add each participant to a list
        for horse in race_df.values:
            horses.append(horse)

        # Add the whole race to a list
        races.append(race_df.values)
    except:
        races.append("DELETE THIS ROW") # Some rows just dont fit... delete the rows afterwards!

# Save participations for further inspection
all_participations_df = pd.DataFrame(data=horses, columns=columns)
all_participations_df.to_csv("csvs/participations.csv", index=False)


# In[11]:


# Replace the cleaned races with the old races in the dataframe
flattened = np.array(races).reshape(1, -1)
flattened_races = []
for dim in flattened:
    for dim2 in dim:
        try:
            flattened_races.append(dim2.reshape(1,-1))
        except:
            flattened_races.append([])

galopp["Horses"] = np.array(flattened_races)
galopp.to_csv("csvs/galopp_cleaned.csv", index=False)


# In[ ]:
