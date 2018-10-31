#!/usr/bin/env python3

from urllib.request import Request, urlopen
import urllib

def translate_str(ip_str, lang):
	print ("Trying to translate....{}".format(ip_str.decode("utf-8")))
	request = Request("https://microsoft-azure-translation-v1.p.mashape.com/translate?from=en&to={}&text={}".format(lang, urllib.parse.quote_plus(ip_str.decode("utf-8"))))	
	
	# Add your API Key in this header
	request.add_header("X-Mashape-Key", "")
	request.add_header("X-Mashape-Host", "microsoft-azure-translation-v1.p.mashape.com")
	request.add_header("Accept", "application/json")
	response = urlopen(request).read()
	response = response.decode("utf-8")
	response = response.split("</string>")[0].split(">")[1]
	return response
	