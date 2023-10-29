from flask import Flask,request,render_template
import requests
app = Flask(__name__)

@app.route('/')
def get_info():
  return render_template('index.html')
  
@app.route('/submit',methods = ['POST'])
def bus_station():
  try:
    url = "https://flixbus2.p.rapidapi.com/trips"
    departure_station = request.form['departure_station']
    arrival_station = request.form['arrival_station']
    date = request.form['date']
    date = date.split('-')
    date = date[::-1]
    date = '.'.join(date)
    adult = request.form['adult']
    children = request.form['children']
    #list of all bus stations and their ids
    bus_list = {
  "london" : "40dfdfd8-8646-11e6-9066-549f350fcb0c",
  "moscow" : "29e8a6b2-9ad1-484e-ae8c-aee9fd831ca6",
  "ljubljana" : "40de8044-8646-11e6-9066-549f350fcb0c",
  "berlin" : "40d8f682-8646-11e6-9066-549f350fcb0c",
  "rome" : "40de90ff-8646-11e6-9066-549f350fcb0c",
  "munich" : "40d901a5-8646-11e6-9066-549f350fcb0c",
  "hamburg" : "40d91e53-8646-11e6-9066-549f350fcb0c",
  "frankfurt" : "40d92162-8646-11e6-9066-549f350fcb0c",
  "stuttgart" : "40d90995-8646-11e6-9066-549f350fcb0c",
  "cologne" : "40d91025-8646-11e6-9066-549f350fcb0c",
  "dusseldorf" : "40d911c7-8646-11e6-9066-549f350fcb0c",
  "dresden" : "40db219f-8646-11e6-9066-549f350fcb0c",
  "hanover" : "40da4ac8-8646-11e6-9066-549f350fcb0c",
  "leipzig" : "40d917f9-8646-11e6-9066-549f350fcb0c",
  "nuremberg" : "40d90d0f-8646-11e6-9066-549f350fcb0c",
  "freiburg" : "40d8ff3b-8646-11e6-9066-549f350fcb0c",
  "dortmund" : "40da382b-8646-11e6-9066-549f350fcb0c",
  "karlsruhe" : "40d912c2-8646-11e6-9066-549f350fcb0c",
  "mannheim" : "40d90c3a-8646-11e6-9066-549f350fcb0c",
  "heidelberg" : "40d9068f-8646-11e6-9066-549f350fcb0c",
  "bremen" : "40da6e70-8646-11e6-9066-549f350fcb0c",
  "essen" : "40da3d5e-8646-11e6-9066-549f350fcb0c",
  "duisburg" : "40da79b3-8646-11e6-9066-549f350fcb0c"
}
    querystring = {
  "from_id" : bus_list[departure_station],  
  "to_id" : bus_list[arrival_station],
  "date":date,
  "adult":adult,
  "children":children,
  "bikes":'0',
  "currency":"EUR"}

    headers = {
  "X-RapidAPI-Key": "1973bac5f8mshf0fd04b7d7d49fbp1dce50jsn56a46a23a197",
  "X-RapidAPI-Host": "flixbus2.p.rapidapi.com"
}

    response = requests.get(url, headers=headers,   params=querystring)

    output = response.json()
    bus_info = output['journeys']
    bus_all_details = []
    if 'error' not in bus_info[0]:
      bus_all_details.append(f"TOTAL {len(bus_info)} BUSES ARE AVAILABLE")
      for i in range(len(bus_info)):

        bus_all_details.append(f"The {i+1}th bus details:")
        bus_all_details.append(f"The bus departs from the bus station: {bus_info[i]['dep_name']}")
  
        bus_all_details.append(f"The bus arrives to the bus station: {bus_info[i]['arr_name']}")
  
        date,time = bus_info[i]['dep_offset'].split('T')
        time = time.split('.')
        time = time[0][:5]
        bus_all_details.append(f'''The bus departs at:
        date: {date}
        Time: {time}''')
  
        date,time = bus_info[i]['arr_offset'].split('T')
        time = time.split('.')
        time = time[0][:5]
        bus_all_details.append(f'''The bus arrives at:
        date: {date}
        time: {time}''')
  
        h,m = bus_info[i]['duration'].split(':')
        bus_all_details.append(f"The bus travels for {h} hours {m} minutes")

        fare = bus_info[i]['fares'][0]
        '''bus_all_details.append(f"Total fare is: {fare['price']}€")'''
        if 'additional_info' not in fare:
          bus_all_details.append("The seats are not available")
        else:
          bus_all_details.append(fare['additional_info'])
        bus_all_details.append('\n')
    else:
        bus_all_details.append(bus_info[0]['message'])
    return render_template('result.html',title = "ALL BUS DETAILS",items = bus_all_details)
  except:
    return render_template('result.html',title = "ENTER DETAILS CORRECTLY OR IF ENTERED CORRECTLY THEN BUSES MIGHT NOT BE PRESENT",items = [])
  
app.run(debug = True)