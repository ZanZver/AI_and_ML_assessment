import sys
try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *

def testFindCoords(dataset):
    start = [-118.249870,34.023630] #1900 S Central Ave, Los Angeles, CA 90011, United States
    dest = [-118.248460,34.040480] #723 San Julian St, Los Angeles, CA 90014, United States

    path = dataset
    cleanDataDf = startup.pd.read_csv("Data/cleanData.csv",index_col=0)
    
    cleanDataDf['LAT'] = cleanDataDf['LAT'].map(lambda x: '%2.4f' % x)
    #cleanDataDf['LON'] = cleanDataDf['LON'].map(lambda x: float(x.replace('\U00002013', '-')))
    cleanDataDf['LON'] = cleanDataDf['LON'].map(lambda x: '%4.3f' % x)
    
    pathDf = startup.pd.DataFrame(path, columns = ['LON','LAT'])
    pathDf['LAT'] = pathDf['LAT'].map(lambda x: '%2.4f' % x)
    #pathDf['LON'] = pathDf['LON'].map(lambda x: float(x.replace('\U00002013', '-')))
    pathDf['LON'] = pathDf['LON'].map(lambda x: '%4.3f' % x)
    
    crimeBasedLocationPath = cleanDataDf.assign(IncleanDataDfLAT=cleanDataDf.LAT.isin(pathDf.LAT).astype(bool))
    crimeBasedLocationPath = crimeBasedLocationPath.assign(IncleanDataDfLON=cleanDataDf.LON.isin(pathDf.LON).astype(bool))
    
    #crimeBasedLocationPath = pathDf.assign(IncleanDataDfLAT=pathDf.LAT.isin(cleanDataDf.LAT).astype(bool))
    #crimeBasedLocationPath = crimeBasedLocationPath.assign(IncleanDataDfLON=pathDf.LON.isin(cleanDataDf.LON).astype(bool))
    
    crimeBasedLocationPath = ((crimeBasedLocationPath.loc[(crimeBasedLocationPath['IncleanDataDfLAT'] == True) & (crimeBasedLocationPath['IncleanDataDfLON'] == True)]))
    #print(len(crimeBasedLocationPath))
    #print(crimeBasedLocationPath.LAT)
    #print(crimeBasedLocationPath.LON)
    #testGetValues()
    print("==================")
    df2 = startup.pd.DataFrame()
    for index, row in crimeBasedLocationPath.iterrows():
        df2 = df2.append(testGetValues(row[26], row[27]))
        #print()
        #print(item.LAT)
        
        
    #print(df2)

    print("==================")

    #n = 10
    print(df2['Desc'].value_counts()[:5].index.tolist())
    
def testGetValues(LAT, LON):
    df = startup.pd.read_csv("Data/cleanData.csv", index_col = 0).head(100)
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

    df2 = startup.pd.DataFrame(startup.np.insert(df.values, 0, values=[now.strftime('%H:%M:%S'), 
    None, None,None,None,None,None,None,LAT,LON], axis=0))

    df2.columns = df.columns
    df = df2

    df['Time OCC'] = startup.pd.to_datetime(df['Time OCC'])
    df['Hour OCC'] = startup.pd.DatetimeIndex(df['Time OCC']).hour
    df['Minute OCC'] = startup.pd.DatetimeIndex(df['Time OCC']).minute
    df['Second OCC'] = startup.pd.DatetimeIndex(df['Time OCC']).second

    df = df.drop(['Time OCC'], axis = 1) 
    df = startup.pd.get_dummies(df, columns=['Hour OCC'], drop_first=False, prefix='Hour')
    df = startup.pd.get_dummies(df, columns=['Minute OCC'], drop_first=False, prefix='Minute')

    df2 = df.head(1)
    df = df.iloc[1:]

    y = df["Crm Cd"]

    del df['Area']
    del df['Rpt Dist No'] 
    del df['Part 1-2']
    del df['Crm Cd']
    del df['Vict age']
    del df['Premis Cd']
    del df['Weapon Used Cd']
    x = df

    del df2['Area']
    del df2['Rpt Dist No'] 
    del df2['Part 1-2']
    del df2['Crm Cd']
    del df2['Vict age']
    del df2['Premis Cd']
    del df2['Weapon Used Cd']

    X_train,X_test,y_train,y_test=startup.train_test_split(x,y,test_size=0.2)

    dtree = startup.DecisionTreeRegressor(max_depth=8, min_samples_leaf=0.13, random_state=3)
    dtree.fit(X_train, y_train)

    startup.DecisionTreeRegressor(criterion='mse', max_depth=8, max_features=None,
            max_leaf_nodes=None, min_impurity_decrease=0.0,
            min_impurity_split=None, min_samples_leaf=0.13,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
                random_state=3, splitter='best')

    # Code Lines 1 to 4: Fit the regression tree 'dtree1' and 'dtree2' 
    dtree1 = startup.DecisionTreeRegressor(max_depth=2)
    dtree2 = startup.DecisionTreeRegressor(max_depth=5)
    dtree1.fit(X_train, y_train)
    dtree2.fit(X_train, y_train)

    # Code Lines 5 to 6: Predict on training data
    tr1 = dtree1.predict(X_train)
    tr2 = dtree2.predict(X_train) 

    #Code Lines 7 to 8: Predict on testing data
    y1 = dtree1.predict(X_test)
    y2 = dtree2.predict(X_test)

    model_rf = startup.RandomForestRegressor(n_estimators=5000, oob_score=True, random_state=100)
    model_rf.fit(X_train, y_train) 

    #print("============================")
    pred = (dtree.predict(df2.values))
    #print("============================")
    
    data = None

    with open('Data/UCR-COMPSTAT062618.json', 'r') as myfile:
        data=myfile.read()

    obj = startup.json.loads(data)
    mocodesData = startup.pd.DataFrame(obj)
    #input = int(451)
    retArr = (mocodesData.iloc[(mocodesData['ID']-pred).abs().argsort()[:5]])
    return retArr