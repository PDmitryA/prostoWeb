from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.files import File
from ask.models import *
from questions.models import UserImaged, Question, Tag, Answer
from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'w-50', 'placeholder': 'Enter your Username here', }),
        max_length=30
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'w-50', 'placeholder': '*******', }),
        min_length=8
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('User is not active')
        else:
            raise forms.ValidationError('Wrong login or password')


class SignupForm(forms.Form):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username here', }),
        max_length=30
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.ru', }),
        max_length=100
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        min_length=8
    )
    password_repeat = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        min_length=8
    )
    avatar = forms.FileField(
        label='Avatar',
        widget=forms.ClearableFileInput(),
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = UserImaged.objects.get(username=username)
            raise forms.ValidationError('Username is already used')
        except UserImaged.DoesNotExist:
            return username

    def clean_password_repeat(self):
        pswd = self.cleaned_data.get('password', '')
        pswd_repeat = self.cleaned_data.get('password_repeat', '')

        if pswd != pswd_repeat:
            raise forms.ValidationError('Passwords does not matched')
        return pswd_repeat

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        try:
            e = UserImaged.objects.get(email=email)
            raise forms.ValidationError('Email is already used')
        except UserImaged.DoesNotExist:
            return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar is not None:
            if 'image' not in avatar.content_type:
                raise forms.ValidationError('Wrong image type')
        return avatar

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        u = UserImaged()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.is_active = True
        u.save()

        if data.get('avatar') is not None:
            u.avatar = data.get('avatar')

        u.save()

        return authenticate(username=u.username, password=password)

    def edit(self, user):
        data = self.cleaned_data
        password = data.get('password')
        user.username = data.get('username')
        user.password = make_password(password)
        user.email = data.get('email')
        user.is_active = True
        user.save()

        if data.get('avatar') is not None:
            user.avatar = data.get('avatar')

        user.save()

        return authenticate(username=user.username, password=password)


class QuestionForm(forms.Form):
    short = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class':'w-75', 'placeholder': 'Enter question title here', }),
        max_length=100
    )
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(
            attrs={'class': 'w-75', 'rows': '13', 'placeholder': 'Add the question description here', }),
        max_length=100000
    )
    tags = forms.CharField(
        label='Tags',
        widget=forms.TextInput(attrs={'class': 'w-75', 'placeholder': 'Tag1,Tag2,Tag3'}),
        required=False
    )

    def check_tag(self, tag):
        if (' ' in tag) or ('\n' in tag) or ('\t' in tag):
            raise forms.ValidationError('Tags contain spaces')
        if ('/' in tag) or ('\\' in tag) or ('?' in tag):
            raise forms.ValidationError('You can use only this symbols -+_~&@*%$')
        return tag

    def parse_tags(self, tags):
        self._tag_list = tags.split(',', 10)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        self.parse_tags(tags)
        for tag in self._tag_list:
            self.check_tag(tag)

    def save(self, user):
        data = self.cleaned_data
        q = Question.manager.create(short=data.get('short'), text=data.get('text'),
                                        author=user)
        q.tags.clear()
        q.save()
        for tag_text in self._tag_list:
            if tag_text is not None and tag_text != '':
                tag = Tag.objects.get_or_create(name=tag_text)
                q.tags.add(tag[0])
        q.save()
        return q


class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-100', 'rows': '5',
                                     'placeholder': 'Do you know the solution?', })
    )

    def save(self, question, user):
        data = self.cleaned_data
        answer = Answer(text=data.get('text'), author=user, question=question)
        answer.save()
        return answer

