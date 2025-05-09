from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Question, Comment
from .forms import CommentForm, QuestionForm
from django.urls import reverse, reverse_lazy

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# CRUD Function
def like_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('stackbase:question-detail', args=[str(pk)]))

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context

class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data()
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        return False

class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = "/"

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        return False

class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'stackbase/question_detail.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stackbase:question-detail', kwargs={'pk': self.kwargs['pk']})

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'stackbase/question_answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stackbase:question-lists')

class QuestionsBySubcategoryView(ListView):
    model = Question
    template_name = 'stackbase/question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        subcategory = self.kwargs['subcategory']
        return Question.objects.filter(tags__icontains=subcategory).order_by('-date_created')  # `created_at` o‘rniga `date_created`

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.kwargs['subcategory']
        return context