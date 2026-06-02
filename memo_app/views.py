from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo
from .forms import MemoForm

# 박홍진 님 담당: 메모 작성 로직
def memo_create(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            # 민승민 님 담당: 작성자 할당 (로그인 기능 완성 전이면 일단 제외 가능)
            if request.user.is_authenticated:
                memo.author = request.user
            memo.save()
            return redirect('memo:list') 
    else:
        form = MemoForm()
    
    # 박동제 님 담당: 템플릿 바인딩
    return render(request, 'memo_app/memo_form.html', {'form': form})