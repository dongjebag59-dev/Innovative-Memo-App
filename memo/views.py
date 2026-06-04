from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import MemoForm
from .models import Category, Memo
from .synonyms import expand_query


@login_required
def memo_list(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "latest")
    selected_category = request.GET.get("category", "").strip()

    memos = Memo.objects.filter(author=request.user)

    if q:
        terms = expand_query(q)
        q_filter = Q()
        for term in terms:
            q_filter |= (
                Q(content__icontains=term) |
                Q(keywords__icontains=term) |
                Q(user_tags__icontains=term)
            )
        memos = memos.filter(q_filter)

    if selected_category and selected_category.isdigit():
        memos = memos.filter(category_id=int(selected_category))

    if sort == "oldest":
        memos = memos.order_by("-is_pinned", "created_at")
    else:
        memos = memos.order_by("-is_pinned", "-created_at")

    categories = Category.objects.order_by("order")

    paginator = Paginator(memos, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "memos": page_obj,
        "categories": categories,
        "selected_category": selected_category,
        "q": q,
        "sort": sort,
    }
    return render(request, "memo/memo_list.html", context)


@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    return render(request, "memo/memo_detail.html", {"memo": memo})


@login_required
def memo_create(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.author = request.user
            memo.save()
            messages.success(request, "메모가 저장되었습니다!")
            return redirect("memo:list")
        messages.error(request, "입력 내용을 확인해 주세요.")
    else:
        form = MemoForm()

    categories = Category.objects.order_by("order")
    return render(request, "memo/memo_form.html", {
        "form": form,
        "is_update": False,
        "categories": categories,
    })


@login_required
def memo_update(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)

    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            messages.success(request, "메모가 수정되었습니다.")
            return redirect("memo:detail", memo_id=memo.id)
        messages.error(request, "입력 내용을 확인해 주세요.")
    else:
        form = MemoForm(instance=memo)

    categories = Category.objects.order_by("order")
    return render(request, "memo/memo_form.html", {
        "form": form,
        "is_update": True,
        "categories": categories,
    })


@require_POST
@login_required
def memo_delete(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    memo.delete()
    messages.success(request, "메모가 삭제되었습니다.")
    return redirect("memo:list")


@require_POST
@login_required
def memo_pin_toggle(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    memo.is_pinned = not memo.is_pinned
    memo.save(update_fields=["is_pinned"])
    next_url = request.POST.get("next", "")
    return redirect(next_url if next_url else "memo:list")
