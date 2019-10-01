import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station   



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Instructions were somewhat unclear. Going to use the 1 year of data that we did in the jupyternotebook, except turned into
#a dictionary and put through flask.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    #The most recent data seems to be from 2017-08-23, so I"ll take the most recent 12 months, which is what I believe is being asked.
    lastDay=session.query(Measurement).order_by(Measurement.id.desc()).first()


    # Calculate the date 1 year ago from the last data point in the database
    firstYear=int(lastDay.date[0:4])-1

    firstDay=str(firstYear)+lastDay.date[4:]



    # Perform a query to retrieve the data and precipitation scores
    mydata=session.query(Measurement).filter(Measurement.date>=firstDay)
    session.close()
    allpercip={}
    for value in mydata:
        allpercip[value.date]=value.prcp

    return jsonify(allpercip)

#Returning a list of dictionaries for the station
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station)

    session.close()


    #Create a list of dictionaries for each of the stations
    AllResults=[]
    for result in results:
        thisResult={}
        thisResult['station']=result.station 
        thisResult['name']=result.name
        thisResult['latitude']=result.latitude
        thisResult["longitutde"]=result.longitude
        thisResult["elevation"]=result.elevation
        AllResults.append(thisResult)


    
    

    return jsonify(AllResults)



@app.route("/api/v1.0/tobs")
def tobs():
        session = Session(engine)

        # Design a query to retrieve the last 12 months of precipitation data and plot the results
        #The most recent data seems to be from 2017-08-23, so I"ll take the most recent 12 months, which is what I believe is being asked.
        lastDay=session.query(Measurement).order_by(Measurement.id.desc()).first()


        # Calculate the date 1 year ago from the last data point in the database
        firstYear=int(lastDay.date[0:4])-1

        firstDay=str(firstYear)+lastDay.date[4:]



        # Perform a query to retrieve the data and precipitation scores
        mydata=session.query(Measurement).filter(Measurement.date>=firstDay)
        session.close()
        fullData=[]
        for result in mydata:
            thisResult={}
            thisResult['date']=result.date
            thisResult['temp']=result.tobs
            fullData.append(thisResult)

        return(jsonify(fullData))

#Take a date, and return the max, min, and average temp between taht date and the en
@app.route("/api/v1.0/<start>")
def mystart(start):
    session = Session(engine)

    mydata=session.query(Measurement).filter(Measurement.date>=start)
    session.close()
    fullData=[]
    for result in mydata:
        fullData.append(result.tobs)
    #Find average of the data
    average=sum(fullData)/len(fullData)
    #Find Max of the data
    maximum=max(fullData)
    #Find Min of the Data
    minimum=min(fullData)

    return("Average: "+str(average)+" Max: "+str(maximum)+" Min: "+str(minimum))




@app.route("/api/v1.0/<start>/<end>")
def start(start,end):
    session = Session(engine)

    mydata=session.query(Measurement).filter(Measurement.date>=start).filter(Measurement.date<=end)
    session.close()
    fullData=[]
    for result in mydata:
        fullData.append(result.tobs)
    #Find average of the data
    average=sum(fullData)/len(fullData)
    #Find Max of the data
    maximum=max(fullData)
    #Find Min of the Data
    minimum=min(fullData)

    return("Average: "+str(average)+" Max: "+str(maximum)+" Min: "+str(minimum))

if __name__ == '__main__':
    app.run(debug=True)