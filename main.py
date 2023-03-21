import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

stations = pd.read_csv("data/stations.txt",
                       skiprows=17,
                       usecols=["STAID", "STANAME                                 "])


@app.route("/")
def home():
    return render_template("home.html", stations=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = f"data/TG_STAID{str(station.zfill(6))}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def about_station(station):
    filename = f"data/TG_STAID{str(station.zfill(6))}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = f"data/TG_STAID{str(station.zfill(6))}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]
    result = result.to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
