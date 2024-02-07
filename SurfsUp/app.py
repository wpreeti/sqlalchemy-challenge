# Import the dependencies.

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station



# Flask
app = Flask(__name__)

@app.route("/")

def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/2016-01-01<br/>"
        f"/api/v1.0/start_date/end_date/2016-01-01/2016-01-07"

    )


@app.route("/api/v1.0/precipitation")

def prcp():

    session = Session(engine)

    sel = [measurement.date, func.max(measurement.prcp)]
    average_rain_fall = session.query(*sel).\
    group_by(measurement.date).\
    order_by(measurement.date).all()

    session.close()

    rainfall_dates = []

    for date, prcp in average_rain_fall:
        rainfall_dict = {}
        rainfall_dict["date"] = date
        rainfall_dict["prcp"] = prcp
        rainfall_dates.append(rainfall_dict)

    return jsonify(rainfall_dates)


@app.route("/api/v1.0/stations")

def stations():

    session = Session(engine)

    station_list = session.query(station.name).all()

    session.close()

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")

def temperatures():

    session = Session(engine)

    temp_data = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= "2016-08-19").\
    filter(measurement.station == "USC00519281").\
    group_by(measurement.date).all()

    session.close()

    temp_dates = []

    for date, tobs in temp_data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_dates.append(temp_dict)

    return jsonify(temp_dates)


#Temp stats

@app.route("/api/v1.0/start_date/<start_date>")

def calc_temps_single_date(start_date):

    session = Session(engine)

    temp_high = session.query(func.max(measurement.tobs)).\
    filter(measurement.date >= start_date)[0][0]

    temp_low = session.query(func.min(measurement.tobs)).\
    filter(measurement.date >= start_date)[0][0]

    temp_avg = round(session.query(func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date)[0][0],2)

    session.close()

    one_date_temp_dict = {}
    one_date_temp_dict["Maximum Temp"] = temp_high
    one_date_temp_dict["Minimum Temp"] = temp_low
    one_date_temp_dict["Average Temp"] = temp_avg


    return jsonify(one_date_temp_dict)



@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")

def calc_temps(start_date, end_date):

    session = Session(engine)

    temp_high_dates = session.query(func.max(measurement.tobs)).\
    filter(measurement.date >= start_date).\
    filter(measurement.date <= end_date)[0][0]

    temp_low_dates = session.query(func.min(measurement.tobs)).\
    filter(measurement.date >= start_date).\
    filter(measurement.date <= end_date)[0][0]

    temp_avg_dates = round(session.query(func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date).\
    filter(measurement.date <= end_date)[0][0],2)

    session.close()

    two_date_temp_dict = {}
    two_date_temp_dict["Maximum Temp"] = temp_high_dates
    two_date_temp_dict["Minimum Temp"] = temp_low_dates
    two_date_temp_dict["Average Temp"] = temp_avg_dates


    return jsonify(two_date_temp_dict)

if __name__ == '__main__':
    app.run(debug=True)