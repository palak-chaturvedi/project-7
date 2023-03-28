# This is the prediction app which predicts the stocks value using two ways
# 1. Using random forest classfier it predicts stock price will go up or down
# 2. Using a Strategy CLass and creating a indicator window it predicts the stock should be bought or sell at the current point of time

# SP folder contains the dataset pertaining to each company which is created at runtime when user calls a particular company.
# models folder contains the prediction models pertaining to each company which is created at runtime when user calls a particular company.

# view.py contains two functions for get and post call the related url.
#predict function predicts the stock up or down and buy or sell using a random forest model and a strategy class
# calculate function is a stock investment calculator which calls the yahoo finance API to calculate the profit and loss of the user.
