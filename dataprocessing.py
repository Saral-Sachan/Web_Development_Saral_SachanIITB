import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_absolute_error as mae, r2_score  #r2_score--.coefficient of determination of how good a ML model is



data = pd.read_csv('C:\\Users\\Saral Sachan\\OneDrive\\Desktop\\Vs codess\\.vscode\\WebDev\\JavaScript\\ITC_WebTeam\\WnCC\\data.csv')
# print(data.head())
# print(data.info())

# defining  new Mathematical metrics (feature engineering) 

# Engagement Rate
# 1. How much are people interacting relative to the views?
data['Engagement_Rate'] = (data['Like_Count'] + data['Comment_Count']) / data['View_Count']

# 2. The Clickbait Exposer: Like-to-View Ratio
# High views but low likes is a massive indicator for clickbait.
data['Like_to_View_Ratio'] = data['Like_Count'] / data['View_Count']

# 3. Disappointment Metric: Comment-to-Like Ratio
# If a video has tons of comments but no likes, people are probably arguing or complaining in the comments.
data['Comment_to_Like_Ratio'] = data['Comment_Count'] / data['Like_Count'].replace(0, 1) # avoid division by zero

# 4. Virality / Clickbait Penalty
# If a channel with 70 subs gets 1,000,000 views, the title did the heavy lifting, not the channel quality.
data['Views_per_Subscriber'] = data['View_Count'] / data['Channel_Subscriber_Count'].replace(0, 1)  # replace(old_val, new_val)-->avoid error while dividing by zero



# Converting Upload_Date to a proper datetime object
data['Upload_Date'] = pd.to_datetime(data['Upload_Date'])
# Create a 'Days_Since_Upload' feature (assuming today is a fixed reference date)
reference_date = pd.to_datetime('2026-03-29')
data['Days_Since_Upload'] = (reference_date - data['Upload_Date']).dt.days #you cannot directly acccess date, month, year as int, so .dt acts like a bridge for access

#Analysizing the TITLE of the video, and speculating the intensions
# Does the title scream for attention?
data['Title_Length'] = data['Video_Title'].apply(len)
data['Is_All_Caps'] = data['Video_Title'].apply(lambda x: 1 if x.isupper() else 0)
data['Has_Exclamation'] = data['Video_Title'].apply(lambda x: 1 if '!' in x else 0)



#Dropping the metrics/columns the the ML model cannot process mathematically directly, drop the non-numeric columns that I've already extracted value from
features_to_drop = ['Video_Title', 'Video_Description', 'Upload_Date']

X = data.drop(columns=features_to_drop + ['Actual_Quality_Score']) # drop Actual_Quality_Score == separating target from features

# Isolate the target variable we are trying to predict
y = data['Actual_Quality_Score']


# ML model--->
#Since we need to predict a continuos number between 0 and 100, I'll be using regression model --> more specifically RandomForestRegressor for better prediction accuracy


#split the dataSet into training(80%) and testing data(20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #random state=42,  CONVENTION

#initializinng the model
model = RandomForestRegressor(n_estimators=100, random_state=42) #100 decision trees; final output-->avg of predictions of all decision trees

#training the model using the data split for training 
model.fit(X_train, y_train)

# prediction of the target
prediction = model.predict(X_test)

#calculate the errors(use mean absolute error)
error = mae(y_test, prediction)

#checking how good the model is
r2 = r2_score(y_test, prediction)

print(f"The error is: {error} and the r2__score is: {r2}")



# Extract the feature importances from the trained model

importances = model.feature_importances_   #this returns an array of numbers, each number signifying the imporatnce of that feature (index acc to input csv) used in making predictions

# Creating a DataFrame to make it easy to read
feature_importance_df = pd.DataFrame({
    'Feature': X.columns,   #X.columns-->names of input features
    'Importance': importances  #number assigned to each feature according to its importance
})

# Sort from most important to least important i.e decending order according to imporatance values
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

print(" Feature Importances--------->")
print(feature_importance_df)
#The first feature in the printed output will be the feature with the heighest importance


# determining the top 10 best tutorials according to actual quality score

# Creating a copy of the original dataframe to store predictions
results_df = data.copy()

# Using the model to predict the score for the entire dataset(X_train + X_test = full dataSet of X)
results_df['Predicted_Score'] = model.predict(X) #generating new col Predicted_Score and dumping predicted values in it

# Sorting the dataframe by the predicted score in descending order (higher predicted actual_quality_score implies better quality tutorial)
top_10_tutorials = results_df.sort_values(by='Predicted_Score', ascending=False).head(10)

print("Top 10 Best Coding Tutorials ------>")
# Printing just the titles and their predicted scores
print(top_10_tutorials[['Video_Title', 'Predicted_Score']])















