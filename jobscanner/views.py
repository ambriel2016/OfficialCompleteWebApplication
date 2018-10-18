from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template import context
from jobscanner import JobDatabase
from jobscanner import GetHTMLDescription
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		# 	form.save creates the new user
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()

	context = {'form': form}
	return render(request, 'registration/register.html', context)


def urlsinput(request):
	if request.method == 'POST':
		user_dict = {}
		job_data=[]
		jobs = []
		URLS = request.POST.get('urltext')
		URLS = URLS.split('https://')
		for URL in URLS:
			if URL.__contains__('www.'):
				nURL = str('https://' + URL)
				# trim tabs spaces and new lines from right and left hand sides of the URL
				nURL = nURL.strip(' \t\r\n')
				# get job title, company name and job text into a dictionary
				job_dict = GetHTMLDescription.GetHTMLDescription.get_desc(nURL)
				#appened the arrary list of job_data with the job_dict
				job_data.append(job_dict)


		# create a dictionary with the user name and the array list of job_data
		user_dict.update({request.user.get_username(): job_data})

		JobDatabase.JobDatabase.process_data(user_dict)
		key_headers = ["Keyword", "Total Sum", "Count Sum"]

		# Reg table
		sql_query = JobDatabase.JobDatabase.sql_query(request.user.get_username())
		db = sqlite3.connect("db.sqlite3")
		cur = db.cursor()
		cur.execute(sql_query)
		reg_table = cur.fetchall()

		# Lemma Table
		lemmcur = db.cursor()
		lemma_query = JobDatabase.JobDatabase.lemma_sql_query(request.user.get_username())
		lemmcur.execute(lemma_query)
		lemma_table = lemmcur.fetchall()

		# job Table
		job_headers = ["Date", "Position", "Company"]
		jobcur = db.cursor()
		jt_query = JobDatabase.JobDatabase.jobtable_sql_query(request.user.get_username())
		jobcur.execute(jt_query)
		job_table = jobcur.fetchall()



		context = ({'table': reg_table, 'h': key_headers, 'ltable': lemma_table, 'jh':job_headers, 'jobtable':job_table})
		return render(request, 'accounts/table.html', context)

	return render(request, 'accounts/urlsinput.html')


def output(request):
	return render(request, 'accounts/output.html')


def dashboard(request):
	return render(request, 'accounts/dashboard.html')


def index(request):
	return render(request, 'accounts/index.html')
