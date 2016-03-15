from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
import hashlib
import uuid
from django.template import loader, Context, Template
import urllib, urllib2

BASE_API = "http://127.0.0.1:8000/garenaet/"

def index(request):
    return HttpResponse("Hello, ET web app!")

def login(request):
	tokenStr = request.COOKIES.get('access_token', '')
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	print 'token: ' + tokenStr
	print 'username: ' + username
	print 'password: ' + password
	if isTokenValid(tokenStr):
		## redirect to profile page
		response = redirect('/et/profile/')
		return response
	else:
		if username and password:
			## login with username and password, redirect to profile page
			respJson = loginBackend(username, password)
			if respJson['error_code'] != 0:
				template = loader.get_template('login.html')
				return HttpResponse(template.render(Context({}), request))
			else:
				##redirect to profile
				response = redirect('/et/profile/')
				response.set_cookie('access_token', respJson['access_token'])
				return response
		else:
			##display login page
			template = loader.get_template('login.html')
			return HttpResponse(template.render(Context({}), request))

def profile(request):
	tokenStr = request.COOKIES.get('access_token', '')
	if tokenStr:
		## call backend profile api
		## render page
		profileResponse = getProfile(tokenStr)
		username = profileResponse['username']
		nickname = profileResponse['nickname']
		context = Context({
			'username' : username,
			'nickname' : nickname
			})
		template = loader.get_template('profile.html')
		return HttpResponse(template.render(context, request))
	else:
		response = redirect('/et/login/')
		return response


def isTokenValid(tokenStr):
	if not tokenStr:
		return False
	else:
		##call back end api /garenaet/check/token/?token=
		url = BASE_API + 'check/token/?token=' + tokenStr
		print 'call: ' + url
		checkReq = urllib2.Request(url)
		response = urllib2.urlopen(checkReq)
		respJson = json.loads(response.read())
		print respJson
		return respJson['error_code'] == 0

def loginBackend(username, password):
	print 'loginBackend...'
	url = BASE_API + 'login/'
	values = {
		'username': username,
		'password': password
	}
	data = json.dumps(values)
	print data
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	respJson = json.loads(response.read())
	print respJson
	return respJson

def getProfile(tokenStr):
	url = BASE_API + 'profile/'
	value = {
		'access_token': tokenStr
	}
	data = json.dumps(value)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	respJson = json.loads(response.read())
	print respJson
	return respJson

