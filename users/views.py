from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomLogin, CustomRegistration

from django.contrib.auth.decorators import login_required

# -------------------------------------
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template


from .models import User


# class SignUpView(CreateView):
#     form_class = CustomRegistration
#     success_url = reverse_lazy("login")
#     template_name = "users/register.html"

def signup(request):
    if request.method == 'POST':
        form = CustomRegistration(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            htmly = get_template('users/acc_active_email.html')
            data = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            html_content = htmly.render(data)
            to_email = form.cleaned_data.get('email')
            subject, from_email, to = 'welcome', 'your_email@gmail.com', to_email

            message = EmailMultiAlternatives(
                subject, html_content, from_email, [to])
            message.attach_alternative(html_content, "text/html")
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            message.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        form = CustomRegistration()
    return render(request, 'users/register.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = CustomRegistration(request.POST)
#         if form.is_valid():
#             # save form in the memory not in database
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             # to get the domain of the current site
#             current_site = get_current_site(request)
#             mail_subject = 'Activation link has been sent to your email id'
#             message = render_to_string('users/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = CustomRegistration()
#     return render(request, 'users/register.html', {'form': form})


class SignIn(CreateView):
    form_class = CustomLogin
    # success_url = reverse_lazy("login")
    template_name = "users/login.html"


@login_required
def home(request):

    print("##############################")
    print(request.user)
    print("##############################")

    return render(request, 'users/home.html')


def activate(request, uidb64, token):
    user = User()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.  <a href="/login"> Login</a>')
    else:
        return HttpResponse('Activation link is invalid!')