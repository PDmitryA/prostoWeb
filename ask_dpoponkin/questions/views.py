from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from questions.forms import LoginForm, SignupForm, QuestionForm, AnswerForm


from questions.models import Question, Answer, Tag, UserImaged

# Create your views here.

#temporary script for generating fields
#import fake
#fake.fakeanswer()

def index(request):

    #from DB!!! 4DZ
    topQuestions = Question.manager.all_new()
    topQuestions = paginate(topQuestions, request, 5)

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'topQuestions': topQuestions, 'topMembers': topMembers, 'topTags': topTags}
    return render(request, 'index/XIndex.html', context)



def answer(request, qid):

    #fromDB!!! 4DZ
    mainQuestion = Question.manager.get(pk = int(qid))

    userAnswers = Answer.manager.all_answers_by_question(qid)

    userAnswers = paginate(userAnswers, request, 5)

    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(mainQuestion, request.user)
            return HttpResponseRedirect(reverse('questions:answer', kwargs={'qid': mainQuestion.pk}))
    else:
        form = AnswerForm()

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'form':form, 'mainQuestion':mainQuestion, 'userAnswers':userAnswers, 'topMembers': topMembers, 'topTags': topTags}
    return render(request, 'answer/answer.html', context)

def login(request):
    redirect = request.GET.get('continue', reverse('questions:index'))

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'topMembers': topMembers, 'topTags': topTags, 'form': form}
    return render(request, 'login/login.html', context)

@login_required(redirect_field_name='continue')
def logout(request):
	redirect = request.GET.get('continue', reverse('questions:index'))
	auth.logout(request)
	return HttpResponseRedirect(redirect)

@login_required(redirect_field_name='continue')
def newQuestion(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(request.user)
            return HttpResponseRedirect(reverse('questions:answer', kwargs={'qid': q.id}))
    else:
        form = QuestionForm()

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'form':form,'topMembers': topMembers, 'topTags': topTags}
    return render(request, 'question/question.html', context)

def register(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('questions:index'))
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('questions:login'))
    else:
        form = SignupForm()

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'topMembers': topMembers, 'topTags': topTags, 'form':form}
    return render(request, 'register/register.html', context)

@login_required(redirect_field_name='continue')
def settings(request):

    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.edit(request.user)
            return HttpResponseRedirect(reverse('questions:settings'))
    else:
        form = SignupForm()

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'form': form, 'topMembers': topMembers, 'topTags': topTags}
    return render(request, 'settings/settings.html', context)

def tagged(request, findTag):

    #from DB!!! 4DZ
    topQuestions = Question.manager.all_questions_by_tag(findTag)
    topQuestions = paginate(topQuestions, request, 5)

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'findTag':findTag, 'topQuestions': topQuestions, 'topMembers': topMembers, 'topTags': topTags}
    return render(request, 'tagged/tagged.html', context)

def hot(request):

    #from DB!!! 4DZ
    topQuestions = Question.manager.all_rate()
    topQuestionsP = paginate(topQuestions, request, 5)

    topMembers = UserImaged.objects.order_by('-rating').all()[:5]

    topTags = Tag.objects.get_popular_tags()

    context = {'topQuestionsP': topQuestionsP, 'topMembers': topMembers, 'topTags': topTags}
    return render(request, 'hot/hot.html', context)

def paginate(objects_list, request, count):
    paginator = Paginator(objects_list, count)
    page = request.GET.get('page')
    try:
        topQuestions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        topQuestions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        topQuestions = paginator.page(paginator.num_pages)

    return topQuestions