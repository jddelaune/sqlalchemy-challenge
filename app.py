# Import the dependencies.
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, desc

# SQLAlchemy 2.0 has a new way of doing queries and maintains the query object as a legacy construct, see
# https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query and consider updating this
# code to the new way later when time permits.

#################################################
# Database Setup
#################################################

# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our sessionmaker
Session = sessionmaker(engine)

#################################################
# Functions
#################################################

def most_recent_date():
    """Return the most recent date in the database that an observation was taken."""

    with Session() as session:
        first_row = session.query(Measurement.date).order_by(desc(Measurement.date)).limit(1)
        latest_date = dt.date.fromisoformat(first_row.scalar())

    return latest_date

def one_year_prev(date):
    """Return the date one year (365 days) before the date given."""

    one_year_prev_date = date - dt.timedelta(days=365)
    return one_year_prev_date

#################################################
# Flask Setup
#################################################
# define the flask object
app = Flask(__name__)
    
#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data. 
    Return a JSON list of temperature observations for the previous year."""
    with Session() as session:
        
        # Find date one year from latest date in dataset
        latest_date = most_recent_date()
        start_date = one_year_prev(latest_date)

        # find most active station
        active_stations_query = session.query(Measurement.station, func.count(Measurement.station))\
            .group_by(Measurement.station)\
            .order_by(func.count(Measurement.station).desc()).all()

        most_active_station = active_stations_query[0][0]

        year_temps_query = session.query(Measurement.date, Measurement.tobs)\
            .filter(Measurement.date >= start_date)\
            .filter(Measurement.station == most_active_station)\
            .all()

    tobs_list = [{'station': most_active_station}]

    for i in year_temps_query:
        temps_dict = {}
        temps_dict.update({'date': i[0], 'temperature': i[1]})
        tobs_list.append(temps_dict)
        
    return jsonify(tobs_list)

@app.route("/api/v1.0/tstats/<start_date>")
@app.route("/api/v1.0/tstats/<start_date>/<end_date>")
def tstats(start_date, end_date=str(most_recent_date())):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature
    from a specified start date to the most recent date in the database."""
    print(end_date)
    print(str(type(end_date)))
    with Session() as session:
        tstats_result = session.query(
            func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start_date)\
            .filter(Measurement.date <= end_date)\
            .first()

    return jsonify(tuple(tstats_result))    

    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date
    # to the end date, inclusive.

@app.route("/api/v1.0/precipitation")
def precip():
    """Return the most recent year's worth of daily precipitation data from the dataset in JSON format"""
    with Session() as session:
        
        # Find date one year from latest date in dataset
        latest_date = most_recent_date()
        start_date = one_year_prev(latest_date)
        
        # Perform a query to retrieve the data and precipitation scores
        last_year_precip = session.query(Measurement.date, func.avg(Measurement.prcp))\
            .filter(Measurement.date >= start_date)\
            .order_by(Measurement.date)\
            .group_by(Measurement.date)\
            .all()
        
    # Iterate through last_year_precip and add each item to a dictionary
    precip_dict = {}
    for i in last_year_precip:
        precip_dict.update({i[0]: i[1]})
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    with Session() as session:
        station_details = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)\
            .order_by(Station.name)\
            .all()
        
    station_list = []
    for i in station_details:
        station_dict = {}
        station_dict.update({'station': i[0], 'name': i[1], 'latitude': i[2], 'longitude': i[3], 'elevation': i[4]})
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/")
def welcome():
    return (
        f'''<h1>Welcome to the Generic API!</h1>
        <p>Available Routes:<br/>
        <ul>
        <li><b>Route 1:</b>
        <ul style="list-style-type:none"><li>/url1</ul><br />
        <li><b>Route 2:</b>
        <ul style="list-style-type:none"><li>/url2</ul>
        </ul></p>'''
    )   

if __name__ == "__main__":
    app.run(debug=True)