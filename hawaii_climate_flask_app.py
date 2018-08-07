import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii2.sqlite", 
                        connect_args={'check_same_thread':False},
                        poolclass=StaticPool)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Flask setup 
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend"
    )

#add precipitation data over a range of days
@app.route("/api/v1.0/precipitation")
def precipitation():
    two_years = dt.datetime.now() - dt.timedelta(days=730)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= two_years).all()
    precip1 = {date: prcp for date, prcp in precipitation}

    return jsonify(precip1)
    
#add weather station data 
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    station_list = []
    for x in results:
        station_dict= {}
        station_dict['stations'] = x.station
        station_list.append(station_dict)
    
    return jsonify(station_list)

#add temperature data over a range of days
@app.route("/api/v1.0/temperature")
def tobs():
    two_years = dt.datetime.now() - dt.timedelta(days=730)
    temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= two_years).all()
    tobs_dict = {date: tobs for date, tobs in temperature}
    
    return jsonify(tobs_dict)

#adding data for selecting a given day of data
@app.route("/api/v1.0/start")
def calc_start(start_date):

    """Temp Min, Temp AVG, and Temp MAX for a given date.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        Temp MIN, Temp AVG, and Temp MAX for start dates equal to or after a given date
    """
    start_date = '2012-02-28'
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    start_dict = {x for start_date, x in start_query}

    return jsonify(start_dict)

#adding temperature data for a specified range of dates
@app.route("/api/v1.0/startend")
def calc_temps(start_date, end_date):
    
    """Temp MIN, Temp AVG, and Temp MAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        Temp MIN, Temp AVG, and Temp MAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return(calc_temps('2012-02-28', '2012-03-05'))
