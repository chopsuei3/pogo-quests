from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import request, redirect, url_for
import csv

pokestopcache = {}
marker_temp = []

# Load quest text
quest_text = "<select name=\"quest\">"
quest_list = []
quest_csv = csv.reader(open("quests.csv","rb"))
for quest in quest_csv:
    quest_text += "<option value=\"" + str(quest[0]) + "\">" + str(quest[1]) + "</option>"
    quest_list.append(str(quest[1]))
quest_text += "</select>"

#print pokestopcache
#print marker_temp

#app = Flask(__name__)
app = Flask(__name__, template_folder="./templates")

# you can also pass the key here if you prefer
GoogleMaps(app, key="AIzaSyAQ4Lysf5zNt-0ZkoeV4vhuXyWVRzGiQU0")

@app.route("/")
def mapview():
	# Load pokestop locations
    try:
        csv_file = csv.reader(open("pokestops.csv","rb"))
    except:
        csv_file = csv.reader(open("data.csv","rb"))
    for row in csv_file:
        pokestopid = int(row[0])
        marker_lat = row[1]
        marker_lon = row[2]
        try:
            quest = row[3]
        except:
            quest = 0
        html_form = "<form action=\"submitdata\">Select quest<br><input type=\"hidden\" name=\"pokestopid\" value=" + str(pokestopid) + ">" + str(quest_text) + "<br><input type=\"submit\" value=\"Submit\"></form>"
        pokestopcache[pokestopid] = {}
        if str(quest) == '0':
            pokestopcache[pokestopid]['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            pokestopcache[pokestopid]['infobox'] = html_form
        else:
            print pokestopid
            pokestopcache[pokestopid]['icon'] = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
            pokestopcache[pokestopid]['infobox'] = 'Quest entered:<br>' + str(quest_list[int(quest)])
        pokestopcache[pokestopid]['lat'] = marker_lat
        pokestopcache[pokestopid]['lng'] = marker_lon
        marker_temp.append(pokestopcache[pokestopid])

    # creating a map in the view
    pokestopmap = Map(
        identifier="pokestopmap",
        lat=37.968193, 
        lng=-122.528441,
        markers = marker_temp,
        style="width:800px;height:600px;"
#        markers=[
#          {
#             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
#             'lat': 37.4419,
#             'lng': -122.1419,
#             'infobox': "<b>Hello World</b>"
#          },
#          {
#             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
#             'lat': 37.4300,
#             'lng': -122.1400,
#             'infobox': "<b>Hello World from other place</b>"
#          }
#        ]
    )
    return render_template('example.html', pokestopmap=pokestopmap)

@app.route("/submitdata")
def submitdata():
    submit_stop = request.args.getlist('pokestopid')[0].encode('ascii')
    submit_quest = request.args.getlist('quest')[0].encode('ascii')
    print "data received", submit_stop, submit_quest
    

    with open('pokestops.csv' ,'w') as outFile:
        fileWriter = csv.writer(outFile)
        with open('data.csv','r') as inFile:
            fileReader = csv.reader(inFile)
            for row in fileReader:
                if str(row[0]) == str(submit_stop):
                    print "found pokestop id in file"
                    row.append(submit_quest) 
                    fileWriter.writerow(row)
                else:
                    fileWriter.writerow(row)


    pokestopmap = Map(
        identifier="pokestopmap",
        lat=37.968193, 
        lng=-122.528441,
        markers = marker_temp,
        style="width:800px;height:600px;")

#    return render_template('example.html', pokestopmap=pokestopmap)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0')
