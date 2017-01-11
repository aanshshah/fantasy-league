import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from s3direct.widgets import S3DirectWidget

class S3DirectUploadForm(forms.Form):
    images = forms.URLField(widget=S3DirectWidget(
        dest='example3',
        html=(
            '<div class="s3direct" data-policy-url="{policy_url}">'
            '  <a class="file-link" target="_blank" href="{file_url}">{file_name}</a>'
            # '  <a class="file-remove" href="#remove">Remove</a>'
            '  <input class="file-url" type="hidden" value="{file_url}" id="{element_id}" name="{name}" />'
            '  <input class="file-dest" type="hidden" value="{dest}">'
            '  <input class="file-input" type="file" />'
            '  <div class="progress progress-striped active">'
            '    <div class="bar"></div>'
            '  </div>'
            '</div>'
        )))

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data