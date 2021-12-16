from flask import Flask, render_template,  request
import sklearn
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
app=Flask(__name__)

standard_to = StandardScaler()
model = joblib.load(open("model.jl","rb"))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if  request.method == 'POST':
        year = int(request.form["years"])
        year = 2021 - year
        Seller_Type_Individual = request.form["Seller_Type_Individual"]
        if Seller_Type_Individual=="Individual":
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0    
        km=int(request.form["km"])
        fuel = request.form["Fuel_Type"]
        if fuel=='Petrol':
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1

        Transmition = request.form["Transmition"]
        if Transmition == 'Mannual':
            Transmition = 1
        else:
            Transmition = 0
        seller=["Delear","Individual"]
        trans=["Manual","Automatic"]        
        price = float(request.form["present_price"])
        Owner = int(request.form["Owner"])
        result = model.predict(np.array([[price,km,Owner,year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmition]]))
        
        if Fuel_Type_Diesel==1:
            return render_template('display.html',result=round(float(result[0]),2),price=price,km=km,Fuel_Type="Diesel",Seller_Type=seller[Seller_Type_Individual],Transmition=trans[Transmition],year=2021-year,Owner=Owner)
        elif Fuel_Type_Petrol==1:
            return render_template('display.html',result=round(float(result[0]),2),price=price,km=km,Fuel_Type="Petrol",Seller_Type=seller[Seller_Type_Individual],Transmition=trans[Transmition],year=2021-year,Owner=Owner)
        else:
            return render_template('display.html',result=round(float(result[0]),2),price=price,km=km,Fuel_Type="CNG",Seller_Type=seller[Seller_Type_Individual],Transmition=trans[Transmition],year=2021-year,Owner=Owner)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)