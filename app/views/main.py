from flask import render_template, jsonify, request
from app import app, models, db
from app.models import RequestType, Service
import random


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/meraki/redirect', methods=['POST'])
def meraki_redirect():
    pass

@app.route('/meraki', methods=['GET'])
def meraki():
    udata = {}
    udata['grant_url'] = request.args.get('base_grant_url')
    udata['continue_url'] = request.args.get('user_grant_url')
    udata['node_mac'] = request.args.get('node_mac')
    udata['client_ip'] = request.args.get('client_ip')
    udata['client_mac'] = request.args.get('client_mac')
    udata['redirect_url'] = unicode(udata['grant_url']) + unicode("&continue_url=") + unicode(udata['continue_url'])
    services = db.session.query(Service).all()
    return render_template('guest/portal.html', data=udata, services=services)

@app.route("/sms", methods=['GET'])
def sms():
	udata = {}
	number = request.args.get('number')
	text = request.args.get('text')
	token = ''
	api_url = 'https://api.tropo.com/1.0/sessions?action=create&token=4f5677505477586774596461677670695a46756d786878566f446541436d4c79796e634a7368556d57635274&myString='+text+'&myNumber='+number
	return jsonify({'url': api_url})

