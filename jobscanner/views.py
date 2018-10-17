from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
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
        jobs = []
        URLS = request.POST.get('urltext')
        URLS = URLS.split('https://')
        for URL in URLS:
            if URL.__contains__('www.'):
                nURL = str('https://' + URL)
                # trim tabs spaces and new lines from right and left hand sides of the URL
                nURL = nURL.strip(' \t\r\n')
                job_description = GetHTMLDescription.GetHTMLDescription.get_desc(nURL)
                jobs.append(job_description)

        # input new user data into inputs table
        user_dict.update({request.user.get_username(): jobs})

        JobDatabase.JobDatabase.process_data(user_dict)
        headers = ["Keyword", "Total Sum", "Count Sum"]

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
        return render(request, 'accounts/table.html', {'table': reg_table}, {'h': headers}, {'ltable': lemma_table})

    return render(request, 'accounts/urlsinput.html')


def output(request):
    return render(request, 'accounts/output.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def index(request):
    return render(request, 'accounts/index.html')
