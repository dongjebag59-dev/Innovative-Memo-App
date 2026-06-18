from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
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

    synonym_expansions = {}
    if q:
        words = q.split()
        combined_filter = Q()
        for word in words:
            terms = expand_query(word)
            extra = [t for t in terms if t.lower() != word.lower()]
            if extra:
                synonym_expansions[word] = extra
            word_filter = Q()
            for term in terms:
                word_filter |= (
                    Q(content__icontains=term) |
                    Q(keywords__icontains=term) |
                    Q(user_tags__icontains=term)
                )
            combined_filter &= word_filter
        memos = memos.filter(combined_filter)

    if selected_category and selected_category.isdigit():
        memos = memos.filter(category_id=int(selected_category))

    if sort == "oldest":
        memos = memos.order_by("-is_pinned", "created_at")
    else:
        memos = memos.order_by("-is_pinned", "-created_at")

    categories = Category.objects.order_by("order").annotate(
        memo_count=Count("memo", filter=Q(memo__author=request.user))
    )

    paginator = Paginator(memos, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "memos": page_obj,
        "categories": categories,
        "selected_category": selected_category,
        "q": q,
        "sort": sort,
        "synonym_expansions": synonym_expansions,
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
        selected_category_id = request.POST.get("category", "")
        if form.is_valid():
            memo = form.save(commit=False)
            memo.author = request.user
            memo.save()
            messages.success(request, "메모가 저장되었습니다!")
            return redirect("memo:detail", memo_id=memo.id)
        messages.error(request, "입력 내용을 확인해 주세요.")
    else:
        form = MemoForm()
        selected_category_id = ""

    categories = Category.objects.order_by("order")
    return render(request, "memo/memo_form.html", {
        "form": form,
        "is_update": False,
        "categories": categories,
        "selected_category_id": selected_category_id,
    })


@login_required
def memo_update(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)

    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        selected_category_id = request.POST.get("category", "")
        if form.is_valid():
            form.save()
            messages.success(request, "메모가 수정되었습니다.")
            return redirect("memo:detail", memo_id=memo.id)
        messages.error(request, "입력 내용을 확인해 주세요.")
    else:
        form = MemoForm(instance=memo)
        selected_category_id = str(memo.category_id) if memo.category_id else ""

    categories = Category.objects.order_by("order")
    return render(request, "memo/memo_form.html", {
        "form": form,
        "is_update": True,
        "categories": categories,
        "selected_category_id": selected_category_id,
        "memo": memo,
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
    safe = url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()})
    return redirect(next_url if safe else "memo:list")
