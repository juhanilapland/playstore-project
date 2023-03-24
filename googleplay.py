#!/usr/bin/env python
# coding: utf-8

# Google Play Store Analysis for Profitable Ideas
# 
# This project is about analyzing a sample from the Google Play Store to come up with creative ideas for apps. The dataset can be found here: https://www.kaggle.com/datasets/lava18/google-play-store-apps
# 
# The following steps:
# 1. Import the csv file
# 2. Separe the header row from the other rows
# 3. Create a function that can present the data cleanly

# In[3]:


from csv import reader

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
google = list(read_file)
google_header = google[0]
google = google[1:]


# In[4]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n')
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(google_header)
print('\n')
explore_data(google, 0, 2, True)


# We see that the Google Play data set little over 10k apps with 13 columns. The columns that might be useful for the purpose of our analysis are 'App', 'Category', 'Reviews', 'Installs', 'Type', 'Price', and 'Genres'.
# 
# The following steps
# 1. Modify rows that have incorrect data
# 2. Identify duplicate apps
# 3. Remove duplicate apps

# In[5]:


print(google[10472])  # incorrect row
print('\n')
print(google_header)  # header
print('\n')
print(google[0])      # correct row


# In[6]:


google[10472].insert(1, 'LIFESTYLE') # adding the category
google[10472][-4] = 'Lifestyle' # adding the genre
google_dict = {} # heading and record as key-value pair to check for fix

for col_name, val in zip(google_header, google[10472]):
    google_dict[col_name] = val

google_dict


# Next is time to create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app.
# Then we ese the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews).

# In[7]:


duplicate_apps = []
unique_apps = []

for app in google:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# In[8]:


reviews_max = {}

for app in google:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[9]:


print('Expected length:', len(google) - 1181)
print('Actual length:', len(reviews_max))


# In[10]:


google_clean = []
already_added = []

for app in google:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        google_clean.append(app)
        already_added.append(name) # make sure this is inside the if block


# In[11]:


explore_data(google_clean, 0, 3, True)


# The following steps:
#     1. Identify and remove Non-English apps

# In[12]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True


# In[13]:


google_english = []

for app in google_clean:
    name = app[0]
    if is_english(name):
        google_english.append(app)

        
explore_data(google_english, 0, 3, True)


# After removing the duplicates and foreign apps, it's time to remove any paid ads, because we are interested in free apps only.

# In[14]:


google_final = []

for app in google_english:
    price = app[7]
    if price == '0':
        google_final.append(app)
        
print(len(google_final))


# Now we have 8409 apps that are unique, English and are freely downloadable. Next is time to build frequency tables to begin the analysis of the most common genres each market.

# In[15]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[16]:


display_table(google_final, 1) # Category


# In[17]:


display_table(google_final, 5) # the Installs columns


# Next we will convert install values to float type. We need to remove commas, plus characters, we also compute the average number of installs for each genre (category).

# In[18]:


categories_google = freq_table(google_final, 1)

for category in categories_google:
    total = 0
    len_category = 0
    for app in google_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# From these genres, communications apps have the most amount of downloads. This still might not be a good market for a new app if the genre is dominated by a few "giants". It's same thing with social apps, which are dominated by Facebook, Snapchat etc. Let's analyze some communication apps more closely.

# In[19]:


for app in google_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# In[21]:


under_100_m = []

for app in google_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times.
# 
# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. 

# In[22]:


for app in google_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# Books and Reference seems like an Interesting One, because it has a wide variety of different apps. It has for example many books about programming topics like "C Programs handbook", R Language Reference Guide etc. 
# The giants in this category are: "Google Play Books and Amazon Kindle".
# Next let's see some apps that have between 1 million and 10 million downloads.

# In[23]:


for app in google_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# Conclusions
# This project was about:
# 1. Importing a dataset sample (csv-file) from Google Play Store 
# 2. Cleaning the dataset (Fix the row[10472])
# 3. Remote the duplicates based on relevance by creating a clean dataset
# 4. Remote the non-English apps from the dataset
# 5. Remote the non-free apps from the dataset
# 6. Create frequency tables to analyze the dataset
# 7. Identify that the genre "Books and Reference" could have potential
# 
# 
# In this project, we analyzed data about Google Play mobile apps with the goal of recommending an app profile that could be profitable.
# 
# We concluded that Books and Reference could be lucrative genre in Google Play Store based on the amount of installed apps with between 1 million and 100 million installations.
