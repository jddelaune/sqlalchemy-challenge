# Import the dependencies.
from flask import flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
# define the flask object
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
    
#################################################
# Flask Routes
#################################################

# /api/v1.0/precipitation

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

# /api/v1.0/stations

# Return a JSON list of stations from the dataset.
# /api/v1.0/tobs

# Query the dates and temperature observations of the most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.

# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.


@app.route("/url")
def func_name():
    pass

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

