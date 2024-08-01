from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import os
import pandas as pd

app = Flask(__name__)
model1 = pickle.load(open("./rf_reg_flight_new.pkl", "rb"))
model2 = pickle.load(open("./gb_reg_flight_new.pkl", "rb"))
model3 = pickle.load(open("./xgb_reg_flight_new.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        journey_weekday = pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").day_name()

        if(journey_weekday == 'Monday'):
            weekday_Monday=1
            weekday_Tuesday=0
            weekday_Wednesday=0
            weekday_Thursday=0
            weekday_Saturday=0
            weekday_Sunday=0
        elif(journey_weekday == 'Tuesday'):
            weekday_Monday=0
            weekday_Tuesday=1
            weekday_Wednesday=0
            weekday_Thursday=0
            weekday_Saturday=0
            weekday_Sunday=0
        elif(journey_weekday=='Wednesday'):
            weekday_Monday=0
            weekday_Tuesday=0
            weekday_Wednesday=1
            weekday_Thursday=0
            weekday_Saturday=0
            weekday_Sunday=0
        elif(journey_weekday == 'Thursday'):
            weekday_Monday=0
            weekday_Tuesday=0
            weekday_Wednesday=0
            weekday_Thursday=1
            weekday_Saturday=0
            weekday_Sunday=0
        elif(journey_weekday == 'Saturday'):
            weekday_Monday=0
            weekday_Tuesday=0
            weekday_Wednesday=0
            weekday_Thursday=0
            weekday_Saturday=1
            weekday_Sunday=0
        elif(journey_weekday=='Sunday'):
            weekday_Monday=0
            weekday_Tuesday=0
            weekday_Wednesday=0
            weekday_Thursday=0
            weekday_Saturday=0
            weekday_Sunday=1
        else:
            weekday_Monday=0
            weekday_Tuesday=0
            weekday_Wednesday=0
            weekday_Thursday=0
            weekday_Saturday=0
            weekday_Sunday=0
        # print("Journey Date : ",journey_day, journey_month,journey_weekday)

        # Departure
        dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",dep_hour, dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", arrival_hour, arrival_min)

        # Duration
        dur_hour = abs(arrival_hour - dep_hour)
        dur_min = abs(arrival_min - dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        total_stops = int(request.form["stops"])
        # print(total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        airline=request.form['airline']
        if(airline=='Air India'):
            Air_India = 1
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (airline=='GoAir'):
            Air_India = 0
            GoAir = 1
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (airline=='Indigo'):
            Air_India = 0
            GoAir = 0
            IndiGo = 1
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
            
        elif (airline=='Jet Airways'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 1
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
            
        elif (airline=='Jet Airways Business'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 1
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0
            
        elif (airline=='Multiple Carriers'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 1
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (airline=='Multiple Carriers Premium Economy'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 1
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (airline=='Spicejet'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 1
            Vistara = 0
            Vistara_Premium_economy = 0

        elif (airline=='Vistara'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 1
            Vistara_Premium_economy = 0

        elif (airline=='Vistara Premium Economy'):
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 1

        else:
            Air_India = 0
            GoAir = 0
            IndiGo = 0
            Jet_Airways = 0
            Jet_Airways_Business = 0
            Multiple_carriers = 0
            Multiple_carriers_Premium_economy = 0
            SpiceJet = 0
            Vistara = 0
            Vistara_Premium_economy = 0

        # print(Jet_Airways,
        #     IndiGo,
        #     Air_India,
        #     Multiple_carriers,
        #     SpiceJet,
        #     Vistara,
        #     GoAir,
        #     Multiple_carriers_Premium_economy,
        #     Jet_Airways_Business,
        #     Vistara_Premium_economy,
        #     Trujet)

        # Source
        # Banglore = 0 (not in column)
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # print(s_Delhi,
        #     s_Kolkata,
        #     s_Mumbai,
        #     s_Chennai)

        # Destination
        # Banglore = 0 (not in column)
        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        
        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'New Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        

        prediction1=model1.predict([[
            total_stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            dur_hour,
            dur_min,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Vistara,
            Vistara_Premium_economy,
            weekday_Monday,
            weekday_Saturday,
            weekday_Sunday,
            weekday_Thursday,
            weekday_Tuesday,
            weekday_Wednesday
        ]])  


        prediction2=model2.predict([[
            total_stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            dur_hour,
            dur_min,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Vistara,
            Vistara_Premium_economy,
            weekday_Monday,
            weekday_Saturday,
            weekday_Sunday,
            weekday_Thursday,
            weekday_Tuesday,
            weekday_Wednesday
        ]]) 


        prediction3=model3.predict([[
            total_stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            dur_hour,
            dur_min,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Vistara,
            Vistara_Premium_economy,
            weekday_Monday,
            weekday_Saturday,
            weekday_Sunday,
            weekday_Thursday,
            weekday_Tuesday,
            weekday_Wednesday
        ]]) 

        mean_price=(prediction1[0]+prediction2[0]+prediction3[0])/3

        output=round(mean_price,2)

        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))
    
    return render_template("home.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from the environment, default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to all interfaces on the specified port