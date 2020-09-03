from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# Create your views here.


def home(request):
    return render(request, 'home/index.html')


def contact_us(request):
    if request.method == "POST":
        from_email = request.POST['contact']
        mail_subject = 'Reply to queries of ' + from_email
        message = request.POST['queries_text']
        to_email = 'yifecommerce@gmail.com'
        send_mail(
            mail_subject,
            message,
            from_email,
            [to_email],
            fail_silently=False,
        )
        return redirect(contact_us)
    return render(request, 'home/contactus.html')
