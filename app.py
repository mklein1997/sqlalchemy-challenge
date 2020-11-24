from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from numpy import mean

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

@app.route("/")
def home():
    print("Recieved request for 'Home' page")
    return (f"Welcome to the SQL Alchemy homepage <br/>"
            f"Available routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/startdate<br/>"
            f"api/v1.0/startend")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    dates = []
    prcps = []
    for date, prcp in results:
        dates.append(date)
        prcps.append(prcp)
    
    precip_dict = dict(zip(dates, prcps))
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    stationobservations = []
    for station, date, tobs in results:
        stationdict = {}
        stationdict['station'] = station
        stationdict['date'] = date
        stationdict['tobs'] = tobs
        stationobservations.append(stationdict)

    return jsonify(stationobservations)

@app.route("/api/v1.0/startdate")
def startdate():
    print("received request for start date input page")
    print("Input a date (YYYY-MM-DD)")
    start = input()
    session = Session(engine)

    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    tempmax = max(results)
    tempmin = min(results)
    tempavg = mean(results)
    tempobs = [tempmax, tempmin, tempavg]


    return jsonify(tempobs)

@app.route("/api/v1.0/startend")
def startend():
    print("Input a start date YYYY-MM-DD")
    start = input()
    print("Input an end date")
    end = input()
    session = Session(engine)
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
    
    tempmax = max(results)
    tempmin = min(results)
    tempavg = mean(results)
    tempobs_startend = [tempmax, tempmin, tempavg]


    return jsonify(tempobs_startend)
    



if __name__ == '__main__':
    app.run(debug=True)