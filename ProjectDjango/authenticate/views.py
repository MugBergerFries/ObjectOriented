from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<img src="https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwi7jtn9t43hAhWFoYMKHUVUAu8QjRx6BAgBEAU&url=https%3A%2F%2Ftvtropes.org%2Fpmwiki%2Fpmwiki.php%2FFunny%2FTheOfficeUS&psig=AOvVaw2XVpc43CMGkYX4efHKFMYk&ust=1553058518588365" alt="W3Schools.com">)
