"""Flask app that connects to firebase and creates PDF report"""
import datetime
from urllib.parse import quote
from urllib.request import urlopen
import json
from flask import Flask, render_template, url_for
from flask_weasyprint import render_pdf
app = Flask(__name__)  # pylint: disable=invalid-name


@app.route('/ROOMS/<room>/<date>/<inp_date_time>', methods=['GET'])
def inspection_report(room=None, date=None, inp_date_time=None):
    """ Makes a Report of inspaction that took place at said time """
    url = "https://hoteltwoway-65c5b.firebaseio.com/Rooms/" + quote(room) + \
        "/" + quote(date) + "/" + quote(inp_date_time)+ ".json?"
    html = urlopen(url).read().decode('utf-8')
    json_object = json.loads(html)
    context = {}
    context['inspection_time'] = datetime.datetime.strptime(
            json_object['Scan-out'], 
            "%b %d, %Y %I:%M:%S %p"
        ) - \
        datetime.datetime.strptime(
            json_object['Scan-in'],
            "%b %d, %Y %I:%M:%S %p"
        )
    context['checklist'] = json_object['Checklist'].items()
    context['scanin'] = json_object['Scan-in']
    context['scanout'] = json_object['Scan-out']
    context['inspector_name'] = json_object['Inspector']
    context['room'] = room
    return render_template('inspection_report.html', **context)


@app.route('/ROOMS/<room>/<date>/<inp_date_time>.pdf')
def inspection_report_pdf(room=None, date=None, inp_date_time=None):
    """ Make a PDF from inspection_report view """
    return render_pdf(url_for(
        'inspection_report',
        room=room,
        date=date,
        inp_date_time=inp_date_time
        ))

def choises_page(base_link, url, breadcrums):
    """ Display a choise page """
    html = urlopen(url).read().decode('utf-8')
    json_object = json.loads(html)
    context = {}
    context['RoomStatus'] = None
    context['breadcrums'] = breadcrums
    context['choises'] = []
    for key, value in json_object.items():
        if key == 'RoomStatus' or key=='Scan-out' or key=='Scan-in':
            continue
        context['choises'].append(
            {"name": key, "link": base_link + quote(key)}
            )
    if base_link == '/ROOMS/':
        context['choises'] = sorted(
            context['choises'], key=lambda k: k['name'])
    return render_template('choises.html', **context)


@app.route('/ROOMS/', methods=['GET'])
def rooms_list():
    """ Display rooms available """
    base_link = '/ROOMS/'
    url = "https://hoteltwoway-65c5b.firebaseio.com/Rooms.json?shallow=true"
    breadcrums = [{'name':'Rooms', 'link':"/ROOMS/"}]
    return choises_page(base_link, url, breadcrums)


@app.route('/ROOMS/<room>/', methods=['GET'])
def room(room):
    """ Display rooms available """
    base_link = '/ROOMS/' + quote(room) + "/"
    url = "https://hoteltwoway-65c5b.firebaseio.com/Rooms/" + \
        quote(room) + ".json?shallow=true"
    breadcrums = [{'name': 'Rooms', 'link': "/ROOMS/"},
                  {'name': room, 'link': "/ROOMS/"+quote(room)}]
    return choises_page(base_link, url, breadcrums)


@app.route('/ROOMS/<room>/<date>/', methods=['GET'])
def room_date(room, date):
    """ Display rooms available """


    base_link = '/ROOMS/' + quote(room) + "/" + quote(date) + "/"
    url = "https://hoteltwoway-65c5b.firebaseio.com/Rooms/" + quote(room) + \
        "/"+quote(date) + ".json?shallow=true"
    breadcrums = [{'name': 'Rooms', 'link': "/ROOMS/"},
                  {'name': room, 'link': "/ROOMS/" + quote(room)},
                  {'name': date, 'link': "/ROOMS/" + quote(date)},
                 ]
    return choises_page(base_link, url, breadcrums)
