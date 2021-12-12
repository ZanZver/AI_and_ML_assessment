import sys
try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

def findCoords(dataset):
    '''
    Input:
        dataset - path of the route user wants to get from location A to location B
    Return:
        none (at the moment), prediction is printed in the terminal
    Function:
        based on the input dataset, create DF that matches locations in crime DF and do prediction on it
        with what could happen to the user based on LAT, LON and time.now

    Test variables:
        origin: 1900 S Central Ave, Los Angeles, CA 90011, United States
        destination: 723 San Julian St, Los Angeles, CA 90014, United States
    '''

    path = dataset
    cleanDataDf = startup.mainData
    
    cleanDataDf['LAT'] = cleanDataDf['LAT'].map(lambda x: '%2.4f' % x)
    cleanDataDf['LON'] = cleanDataDf['LON'].map(lambda x: '%4.3f' % x)
    
    pathDf = startup.pd.DataFrame(path, columns = ['LON','LAT'])
    pathDf['LAT'] = pathDf['LAT'].map(lambda x: '%2.4f' % x)
    pathDf['LON'] = pathDf['LON'].map(lambda x: '%4.3f' % x)
    
    crimeBasedLocationPath = cleanDataDf.assign(IncleanDataDfLAT=cleanDataDf.LAT.isin(pathDf.LAT).astype(bool))
    crimeBasedLocationPath = crimeBasedLocationPath.assign(IncleanDataDfLON=cleanDataDf.LON.isin(pathDf.LON).astype(bool))
    
    crimeBasedLocationPath = ((crimeBasedLocationPath.loc[(crimeBasedLocationPath['IncleanDataDfLAT'] == True) 
                                                          & (crimeBasedLocationPath['IncleanDataDfLON'] == True)]))
  
    print("==================")
    df2 = startup.pd.DataFrame()
    processedItem = 1
    for item, row in crimeBasedLocationPath.iterrows():
        print("Processing item: " + str(processedItem) + "/" + str(len(crimeBasedLocationPath)))
        X_train,X_test,y_train,y_test,predModel = splitData(row[26], row[27]) #add predDf
        df2 = df2.append(trainRandomForest(X_train,X_test,y_train,y_test,predModel,processedItem))
        processedItem += 1

    print("==================")
    print("Prediction:")
    print(df2['Desc'].value_counts()[:5].index.tolist())
    print("==================")
    
def splitData(LAT, LON):
    '''
    Input:
        LAT and LON
    Return:
        X_train, X_test, y_train, y_test and encoded time now (as dfCurrentTime)
    Function:
        Creates a model based on startup.mainData, values that are inside are LAT, LON, time and crime ID (so what could happen to you)
    '''
    df = startup.mainData
    df = df.drop_duplicates()
    
    del df['DR_NO']
    del df['Date Rptd']
    del df['Date OCC']
    del df['Area name']
    del df['Crm Cd Desc']
    del df['Mocodes']
    del df['Vict sex']
    del df['Vict descent']
    del df['Premis Desc'] 
    del df['Weapon Desc']
    del df['Status']
    del df['Status Desc']
    del df['Crm Cd 1']
    del df['Crm Cd 2']
    del df['Crm Cd 3']
    del df['Crm Cd 4']
    del df['Location']
    del df['Cross Street']
    now = startup.datetime.now()
    
    # df2 is just encoding of the time now (so it can be later used), df is actual model encoding. Due to time / performance efficiency, 
    # time is encoded together (so time now and other time), but it is later split
    dfCurrentTime = startup.pd.DataFrame(startup.np.insert(df.values, 0, values=[now.strftime('%H:%M:%S'), 
    None, None,None,None,None,None,None,LAT,LON], axis=0)) # Labels in the df: Time OCC,Area,Rpt Dist No,Part 1-2,Crm Cd,Vict age,Weapon Used Cd,LAT,LON

    dfCurrentTime.columns = df.columns 
    df = dfCurrentTime
    
    # Encode the time (binary)
    df['Time OCC'] = startup.pd.to_datetime(df['Time OCC'])
    df['Hour OCC'] = startup.pd.DatetimeIndex(df['Time OCC']).hour
    df['Minute OCC'] = startup.pd.DatetimeIndex(df['Time OCC']).minute
    df['Second OCC'] = startup.pd.DatetimeIndex(df['Time OCC']).second

    df = df.drop(['Time OCC'], axis = 1) # Time is now encoded, so label "Time OCC" can be dropped
    df = startup.pd.get_dummies(df, columns=['Hour OCC'], drop_first=False, prefix='Hour')
    df = startup.pd.get_dummies(df, columns=['Minute OCC'], drop_first=False, prefix='Minute')

    '''
    How time is encoded:
    Hour:
        24 new columns are created (name 0-23), so if the hour is 15, column with 15 will have 1 in it and other columns will have 0
    Minute:
        60 new columns are created (name 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55). If the minute is 42, column 40 will have 1 in it, others will have 0
    Second:
        60 new columns are created (name 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55). If the second is 42, column 40 will have 1 in it, others will have 0
    '''
    
    dfCurrentTime = df.head(1) # Get the time now encoded 
    df = df.iloc[1:] # Drop the first row, it is not needed

    y = df["Crm Cd"] # Have crime Cd (ID num) as predicted number output

    # Drop other unnecessary data
    del df['Area']
    del df['Rpt Dist No'] 
    del df['Part 1-2']
    del df['Crm Cd']
    del df['Vict age']
    del df['Premis Cd']
    del df['Weapon Used Cd']
    x = df # Save model to x

    # Drop the same data as in df
    del dfCurrentTime['Area']
    del dfCurrentTime['Rpt Dist No'] 
    del dfCurrentTime['Part 1-2']
    del dfCurrentTime['Crm Cd']
    del dfCurrentTime['Vict age']
    del dfCurrentTime['Premis Cd']
    del dfCurrentTime['Weapon Used Cd']

    X_train,X_test,y_train,y_test=startup.train_test_split(x,y,test_size=0.2) # Split to to 80% train and 20% test
    return (X_train,X_test,y_train,y_test,dfCurrentTime) # Return test, train and encoded time now

def trainDecisionTree(X_train,X_test,y_train,y_test):
    dtree = startup.DecisionTreeRegressor(max_depth=8, min_samples_leaf=0.13, random_state=3)
    dtree.fit(X_train, y_train)

    startup.DecisionTreeRegressor(criterion='mse', max_depth=8, max_features=None,
            max_leaf_nodes=None, min_impurity_decrease=0.0,
            min_impurity_split=None, min_samples_leaf=0.13,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
                random_state=3, splitter='best')

    # Fit the regression tree 'dtree1' and 'dtree2' 
    dtree1 = startup.DecisionTreeRegressor(max_depth=2)
    dtree2 = startup.DecisionTreeRegressor(max_depth=5)
    dtree1.fit(X_train, y_train)
    dtree2.fit(X_train, y_train)

    # Predict on training data
    tr1 = dtree1.predict(X_train)
    tr2 = dtree2.predict(X_train) 

    # Predict on testing data
    y1 = dtree1.predict(X_test)
    y2 = dtree2.predict(X_test)
    
    print("++++++++++++++")
    print("DecisionTree results train model:")
    print("Sqrt: " + str(startup.np.sqrt(startup.mean_squared_error(y_train,tr1))))
    print("R2 score: " + str(startup.r2_score(y_train, tr1)))
    
    # Print RMSE and R-squared value for regression tree 'dtree1' on testing data
    print("Results results test model:")
    print("Sqrt: " + str(startup.np.sqrt(startup.mean_squared_error(y_test,y1))))
    print("R2 score: " + str(startup.r2_score(y_test, y1)))

def trainRandomForest(X_train,X_test,y_train,y_test,predictDataset,processedItem):
    '''
    Input: 
        X_train,X_test,y_train,y_test,predictDataset (LAT, LON, time now encoded)
    Return:
        array of top 5 situations / crimes that you could encounter at that location (LAT, LON) now
    Function:
        it creates a model of random forest, train it and predict it
    '''
    model_rf = startup.RandomForestRegressor(n_estimators=5000, oob_score=True, random_state=100)
    model_rf.fit(X_train, y_train) 

    pred = (model_rf.predict(predictDataset.values))
    
    print("++++++++++++++")
    print("RandomForest results train model:")
    pred_train_rf = model_rf.predict(X_train)
    print("Sqrt: " + str(startup.np.sqrt(startup.mean_squared_error(y_train, pred_train_rf))))
    print("R2 score: " + str(startup.r2_score(y_train, pred_train_rf)))
    print("Results test model:")
    pred_test_rf = model_rf.predict(X_test)
    print("Sqrt: " + str(startup.np.sqrt(startup.mean_squared_error(y_test, pred_test_rf))))
    print("R2 score: " + str(startup.r2_score(y_test, pred_test_rf)))
    
    
    ####
    #from sklearn.tree import export_graphviz
    #import graphviz
    #import os
    try:
        print("Plotting tree"+str(processedItem))
        filename = str('Data/trees/tree' + str(processedItem) + '.dot')
        startup.export_graphviz(model_rf.estimators_[0],
                        feature_names=X_train.columns,
                        filled=True,
                        rounded=True,
                        out_file=filename)
        startup.graphviz.render('dot', 'png', filename) 
    except Exception as e:
        print("Error plotting tree"+str(processedItem))
        print(e)
        
    print("++++++++++++++")
    ####
    
    ucrDF = startup.pd.DataFrame(startup.ucrData) #get the UCR codes from main
    retArr = (ucrDF.iloc[(ucrDF['ID']-pred).abs().argsort()[:5]]) #translate UCR codes from prediction and get top 5 occuring
    return retArr