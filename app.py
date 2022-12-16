from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)  #creating the object of flask

app = Flask("car_model")
model = pickle.load(open('model.pkl', 'rb'))
car=pd.read_csv('car data.csv')

#defining html file to get user input
@app.route('/',methods=['GET','POST'])#mapping the URLs to a specific function.... It will will handle the logic for that URL
#entry Point of the Application
def index():#Index function which will run
    companies=sorted(car['Car_Name'].unique())
    companies.insert(0,'Select Company')
    return render_template('index.html',companies=companies)# going to the html page And passing the Catogries 

#defining Html file to get user input 
@app.route("/predict", methods=['POST'])
def predict():#pridiction function will run from hear
    Fuel_Type_Diesel=0
    if request.method == 'POST':

        company=request.form.get('company')
        Year = int(request.form['Year'])
        Year = 2022 - Year
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']

        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0

        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0

        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Mannual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0

         
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output=round(prediction[0],2)

        if output<0:
            return render_template('index.html',prediction_text=" Sorry you cannot sell this car. ")

        else:
            return render_template('index.html',prediction_text="✅ You Can Sell the Car at {} lakhs ".format(output))

    else:
        return render_template('index.html')
if __name__=="__main__":
    app.run(debug=True)
