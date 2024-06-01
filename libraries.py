#3/27/2024
import pathlib
import textwrap
import google.generativeai as genai
import PyPDF2
import docx
from IPython.display import display
from IPython.display import Markdown
import google.generativeai as genai
import json
import os
from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django import forms
from django.http import HttpResponseRedirect
import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import storage
import requests
from django.shortcuts import render,redirect
import pyrebase
from django import forms
import os
import json
import urllib.request
import tempfile
import docx
import sys
import tempfile
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required