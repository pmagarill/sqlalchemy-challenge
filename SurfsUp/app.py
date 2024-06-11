# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation data from previous year
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation_query_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(first_date)()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in precipitation_query_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all tobs
    all_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= first_date()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in all_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)    
    
    # Make a list to query (min/avg/max temp)
    results=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Query the data from start date to the most recent date
    start_data = session.query(*results).filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    start_list = list(np.ravel(start_data))

    # Close the session                   
    session.close()

    # Return a list of jsonified minimum, average and maximum temperatures for a specific start date
    return jsonify(start_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_dates(start, end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)    
    
    # Make a list to query (min/avg/max temp)
    results=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Query the data from start date to the end date
    start_end_data = session.query(*results).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    # Convert list of tuples into normal list
    start_end_list = list(np.ravel(start_end_data))

    # Close the session                   
    session.close()

    # Return a list of jsonified minimum, average and maximum temperatures for a specific start-end date range
    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)