from .models               import Question, Answer
from django.shortcuts      import render, get_object_or_404, redirect
from django.utils          import timezone
from .forms                import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib        import messages


def index(request):
    """
    목록출력
    """
    page            = request.GET.get('page','1') #페이지
    question_list   = Question.objects.order_by('-create_date')# 조회
    paginator       = Paginator(question_list, 10) #페이지당 10개씩 보여주기
    page_obj        = paginator.get_page(page)

    context         = {'question_list' : page_obj}

    return render(request, 'board/question_list.html', context)

def detail(request, question_id):
    """
     내용 출력
    """

   # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) 
    context  = {'question' : question}
    return render(request, 'board/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
     답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'board/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'수정권한이 없습니다')
        return redirect('board:detail',question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer' : answer, 'form' : form }
    return render(request, 'board/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')

    else:
        answer.delete()
    return redirect('board:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def question_create(request):
    """
    질문등록
    """
    if request.method == 'POST' :
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'board/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문수정
    """

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail',question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request,'삭제권한이 없습니다.')
        return redirect('board:detail',question_id=question.id)
    question.delete()
    return redirect('board:index')
