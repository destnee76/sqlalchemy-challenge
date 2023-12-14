# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///surfsup/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# -Start at the homepage.
# -List all the available routes.

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and precipitation observations from the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2017-08-23').all()

    # Convert the query results to a dictionary
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query for the list of stations
    results = session.query(Station.station, Station.name).all()

    # Convert the query results to a dictionary
    station_list = []
    for station, name in results:
        station_dict = {}
        station_dict['Station'] = station
        station_dict['Name'] = name
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query for the dates and temperature observations of the most active station for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2017-08-23').all()

    # Convert the query results to a dictionary
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

# 5 /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")

def get_temps_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def get_temps_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)