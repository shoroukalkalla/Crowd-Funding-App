from dataclasses import field
from pyexpat import model
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView


from .forms import CustomLogin, CustomRegistration, Profile

from django.contrib.auth.decorators import login_required

# -------------------------------------
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.contrib.auth import views as auth_views

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from projects.models import Project, ProjectImage

from django.core.exceptions import PermissionDenied

from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import add_message, INFO, ERROR


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
            message.send()
            add_message(
                request, INFO, 'Please confirm your email address to complete the registration')
            return redirect('/')
    else:
        form = CustomRegistration()

    return render(request, 'users/register.html', {'form': form})


class SignIn(auth_views.LoginView):
    form_class = CustomLogin
    template_name = "registration/login.html"


@login_required
def home(request):
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
        add_message(
            request, INFO, 'Thank you for your email confirmation. Now you can login your account')
        return redirect('/login')
    else:
        add_message(request, ERROR, 'Activation link is invalid!')
        return redirect('/login')


def profile(request):
    return render(request, 'users/profile.html')


class EditProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = Profile
    template_name = "users/profile.html"

    queryset = User.objects.all()

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")

    def get_queryset(self):
        print(self.request.user.id)
        if self.kwargs['pk'] != str(self.request.user.id):
            raise PermissionDenied()
        return User.objects.filter(id=self.request.user.id)

    def get_success_message(self, cleaned_data):
        return "Account was updated"


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("login")

    def get_success_message(self, cleaned_data):
        return "Account was deleted"


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = '/'

    def get_success_message(self, cleaned_data):
        return "Your password was changed"


class PasswordReset(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/reset_password.html'
    success_url = '/'

    def get_success_message(self, cleaned_data):
        return "Password reset sent"


class PasswordResetSet(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'users/set_password.html'
    success_url = '/'

    def get_success_message(self, cleaned_data):
        return "Your password has been set. You may go ahead and log in now."

def get_latest_projects():
    latest_projects_array = []
    latest_projects=Project.objects.order_by('-id')[:5]
    for project in latest_projects :
        project_image=ProjectImage.objects.filter(project_id=project.id).first()
        data = {'project':project,'image':project_image}
        latest_projects_array.append(data)
    return latest_projects_array


def get_top_latest_projects(request):
    top_projects_array = []
    projects = Project.objects.all()
    for project in projects:
        project_rate = project.averageReview()
        project_image = ProjectImage.objects.filter(
            project_id=project.id).first()
        data = {'project': project, 'image': project_image,
                'average_rate': project_rate}
        top_projects_array.append(data)
    top_projects_array = sorted(
        top_projects_array, key=lambda k: k['average_rate'], reverse=True)

    return render(request, 'users/home.html', {'top_projects': top_projects_array,
                                               'latest_projects': get_latest_projects()})
