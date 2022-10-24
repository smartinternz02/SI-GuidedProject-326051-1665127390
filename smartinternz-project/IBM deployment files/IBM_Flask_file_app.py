from flask import Flask, render_template, request
app = Flask(__name__)
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "mNchOQo_3dIJ3QGdbWaZbzeCZ3lB8b1bg85GI1c7s647"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


model = pickle.load(open('risk.pkl','rb'))

@app.route('/')
def helloworld():
    return render_template("base.html")
@app.route('/assesment')
def prediction():
    return render_template("index.html")

@app.route('/risk', methods = ['POST'])
def admin():

    p= request.form["age"]

    q= request.form["gender"]
    if (q == 'f'):
        q=0
    if (q == 'm'):
        q=1
   
    r= request.form["job"]
    if (r == 'un'):
        r=0
    if (r == 'ur'):
        r=1
    if (r == 'sk'):
        r=2
    if (r == 'hs'):
        r=3
    
    s= request.form["housing"]
    if (s == 'own'):
        s=1
    if (s == 'free'):
        s=0
    if (s == 'rent'):
        s=2

    t= request.form["saving"]
    if (t == 'l'):
        t=0
    if (t == 'm'):
        t=1
    if (t == 'qr'):
        t=2
    if (t == 'r'):
        t=3

    u= request.form["checking"]
    if (u == 'lt'):
        u=0
    if (u == 'mo'):
        u=1
    if (u == 'ri'):
        u=2

    v= request.form["credit"]
    w= request.form["duration"]  

    x= request.form["purpose"]
    if (x == 'bu'):
        x=0
    if (x == 'car'):
        x=1
    if (x == 'da'):
        x=2
    if (x == 'edu'):
        x=3
    if (x == 'fe'):
        x=4
    if (x == 'rtv'):
        x=5
    if (x == 'rep'):
        x=6
    if (x == 'vo'):
        x=7
    y=[[int(p),int(q),int(r),int(s),int(t),int(u),int(v),int(w),int(x)]]   
    payload_scoring = {"input_data": [{"field": [["age","gender","job","housing","saving","checking","credit","duration","purpose"]], "values": y}]}     
    # a = model.predict(y)
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/344a0509-9531-413a-aa1a-509c569e1d2d/predictions?version=2022-10-20', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    predictions=response_scoring.json()
    print(predictions['predictions'][0]['values'][0][0])
    if (predictions['predictions'][0]['values'][0][0] == "bad"):
         return render_template("predbad.html", z = predictions['predictions'][0]['values'][0][0])

    if (predictions['predictions'][0]['values'][0][0] == "good"):
         return render_template("predgood.html", z = predictions['predictions'][0]['values'][0][0])


if __name__ == '__main__':
    app.run(debug = True)