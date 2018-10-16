from django.shortcuts import render


# Create your views here.
def signup(request):
    return render(request, 'accounts/signup.html')


def signin(request):
    return render(request, 'accounts/signin.html')


def logout(request):
    # TODO need to route to home page and don't forget to signout
    # and don't forget to signout
    return render(request, '')


def urlsinput(request):
    return render(request, 'accounts/urlsinput.html')


def output(request):
    return render(request, 'accounts/output.html')
