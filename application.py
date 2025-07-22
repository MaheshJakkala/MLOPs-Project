from flask import Flask,render_template,request
import json
import joblib
from config.paths_config import*

app = Flask(__name__)

model = joblib.load(MODEL_SAVE_PATH)

@app.route("/" , methods = ["GET","POST"])
def home():
    if request.method == 'POST':
        try:
            arrival_delay = float(request.form["Arrival Delay"])
            departure_delay = float(request.form["Departure Delay"])
            flight_distance = float(request.form["Flight Distance"])

            delay_ratio = (arrival_delay+departure_delay)/(flight_distance+1)

            data = [
                int(request.form["Online Boarding"]),
                int(request.form["Inflight wifi service"]),
                delay_ratio,
                int(request.form["Class"]),
                int(request.form["Type of Travel"]),
                int(request.form["Inflight entertainment"]),
                int(request.form["Seat comfort"]),
                flight_distance,
                int(request.form["Leg room service"]),
                int(request.form["On-board service"]),
                int(request.form["Ease of Online Booking"]),
                int(request.form["Cleanliness"]),
            ]

            prediction = model.predict([data])
            output = prediction[0]
            print(output)

            return render_template("index.html",prediction=output)
        except Exception as e:
            return render_template("index.html",error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    # app.run(debug=True)