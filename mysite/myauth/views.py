from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from .models import Profile

class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        return response

class UserLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value {value!r}')


def set_session_view(request: HttpRequest):
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set')

def get_session_view(request: HttpRequest):
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value {value!r}')


class UsersList(ListView):
    template_name = 'myauth/users-list.html'
    context_object_name = 'profiles'
    queryset = Profile.objects.all()


class UserDetailsView(DetailView):
    template_name = 'myauth/about-me.html'
    model = User
    context_object_name = 'user'


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ('avatar',)

    def test_func(self):
        if self.request.user.is_staff or self.request.user.pk == self.get_object().user_id:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse(
            "myauth:user_detail",
            kwargs={"pk": self.object.user.pk},
        )
