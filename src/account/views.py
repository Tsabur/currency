from account.forms import MyPasswordChangeForm, UserRegistrationForm
from account.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View


# class MyProfile(LoginRequiredMixin, UpdateView):
#     queryset = User.objects.filter(is_active=True)
#     fields = ('first_name', 'last_name')
#     success_url = reverse_lazy('index')
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(id=self.request.user.id)
#         # WRONG return queryset.get(id=self.request.user.id)


class MyProfile(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name')
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user


class SignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')


class ActivateUser(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if user.is_active:
            pass
        else:
            user.is_active = True
            user.save(update_fields=('is_active', ))
        return redirect('index')


class MyPasswordChangeView(UpdateView):
    model = User
    form_class = MyPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('index')
