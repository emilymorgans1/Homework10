import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

from flask import Flask, jsonify
app = Flask(__name__)
import warnings
warnings.filterwarnings('ignore')
# We can view all of the classes that automap found
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start_date/end_date<br/>"
             )
@app.route("/api/v1.0/precipitation")
def percipitation():
    last_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    last_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(Station.station).all()
    stations = list(results)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    temp_record= session.query(Measurement.tobs).filter(Measurement.station =="USC00519281").filter(Measurement.date >= last_year).all()
    temp = list(temp_record)
    return jsonify(temp)

@app.route("/api/v1.0/temp/<start_date>/")
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
#2012-02-28', '2012-03-05
def start_end(start_date="2012-02-28", end_date = "2012-03-05"):
    select = [(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))]
    if not end_date: 
        results1 = session.query(*select).filter(Measurement.date >= start_date).all()
        temps = list(results1)
    return jsonify(temps)
    results2 = session.query(*select).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temps2 = list(results2)
    return jsonify(temps2)
   
if __name__ == "__main__":
    app.run(debug=True)