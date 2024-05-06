from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required, teacher_required
from accounts.models import User, Student
from .forms import SessionForm, TermForm, NewsAndEventsForm
from .models import NewsAndEvents, ActivityLog, Session, Term


# ########################################################
# News & Events
# ########################################################
@login_required
def home_view(request):
    items = NewsAndEvents.objects.all().order_by("-updated_date")
    context = {
        "title": "News & Events",
        "items": items,
    }
    return render(request, "core/index.html", context)


@login_required
@admin_required
def dashboard_view(request):
    logs = ActivityLog.objects.all().order_by("-created_at")[:10]
    gender_count = Student.get_gender_count()
    context = {
        "student_count": User.objects.get_student_count(),
        "teacher_count": User.objects.get_teacher_count(),
        "superuser_count": User.objects.get_superuser_count(),
        "males_count": gender_count["M"],
        "females_count": gender_count["F"],
        "logs": logs,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def post_add(request):
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been uploaded."))
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm()
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Add Post",
            "form": form,
        },
    )


@login_required
@teacher_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been updated."))
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Edit Post",
            "form": form,
        },
    )


@login_required
@teacher_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + " has been deleted."))
    return redirect("home")


# ########################################################
# Session
# ########################################################
@login_required
@teacher_required
def session_list_view(request):
    """Show list of all sessions"""
    sessions = Session.objects.all().order_by("-is_current_session", "-session")
    return render(request, "core/session_list.html", {"sessions": sessions})


@login_required
@teacher_required
def session_add_view(request):
    """check request method, if POST we add session otherwise show empty form"""
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_session"
            )  # returns string of 'True' if the user selected Yes
            print(data)
            if data == "true":
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, "Session added successfully. ")
            return redirect("session_list")

    else:
        form = SessionForm()
    return render(request, "core/session_update.html", {"form": form})


@login_required
@teacher_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        data = form.data.get("is_current_session")
        if data == "true":
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()

            if form.is_valid():
                form.save()
                messages.success(request, "Session updated successfully. ")
                return redirect("session_list")
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, "Session updated successfully. ")
                return redirect("session_list")

    else:
        form = SessionForm(instance=session)
    return render(request, "core/session_update.html", {"form": form})


@login_required
@teacher_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if session.is_current_session:
        messages.error(request, "You cannot delete current session")
        return redirect("session_list")
    else:
        session.delete()
        messages.success(request, "Session successfully deleted")
    return redirect("session_list")


# ########################################################


# ########################################################
# Term
# ########################################################
@login_required
@teacher_required
def term_list_view(request):
    terms = Term.objects.all().order_by("-is_current_term", "-term")
    return render(
        request,
        "core/term_list.html",
        {
            "terms": terms,
        },
    )


@login_required
@teacher_required
def term_add_view(request):
    if request.method == "POST":
        form = TermForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_term"
            )  # returns string of 'True' if the user selected Yes
            if data == "True":
                term = form.data.get("term")
                ss = form.data.get("session")
                session = Session.objects.get(pk=ss)
                try:
                    if term.objects.get(term=term, session=ss):
                        messages.error(
                            request,
                            term
                            + " term in "
                            + session.session
                            + " session already exist",
                        )
                        return redirect("add_term")
                except:
                    terms = Term.objects.all()
                    sessions = Session.objects.all()
                    if terms:
                        for term in terms:
                            if term.is_current_term == True:
                                unset_term = Term.objects.get(
                                    is_current_term=True
                                )
                                unset_term.is_current_term = False
                                unset_term.save()
                        for session in sessions:
                            if session.is_current_session == True:
                                unset_session = Session.objects.get(
                                    is_current_session=True
                                )
                                unset_session.is_current_session = False
                                unset_session.save()

                    new_session = request.POST.get("session")
                    set_session = Session.objects.get(pk=new_session)
                    set_session.is_current_session = True
                    set_session.save()
                    form.save()
                    messages.success(request, "Term added successfully.")
                    return redirect("term_list")

            form.save()
            messages.success(request, "Term added successfully. ")
            return redirect("term_list")
    else:
        form = TermForm()
    return render(request, "core/term_update.html", {"form": form})


@login_required
@teacher_required
def term_update_view(request, pk):
    term = Term.objects.get(pk=pk)
    if request.method == "POST":
        if (
            request.POST.get("is_current_term") == "True"
        ):  # returns string of 'True' if the user selected yes for 'is current term'
            unset_term = Term.objects.get(is_current_term=True)
            unset_term.is_current_term = False
            unset_term.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()
            new_session = request.POST.get("session")
            form = TermForm(request.POST, instance=term)
            if form.is_valid():
                set_session = Session.objects.get(pk=new_session)
                set_session.is_current_session = True
                set_session.save()
                form.save()
                messages.success(request, "Term updated successfully !")
                return redirect("term_list")
        else:
            form = TermForm(request.POST, instance=term)
            if form.is_valid():
                form.save()
                return redirect("term_list")

    else:
        form = TermForm(instance=term)
    return render(request, "core/term_update.html", {"form": form})


@login_required
@teacher_required
def term_delete_view(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if term.is_current_term:
        messages.error(request, "You cannot delete current term")
        return redirect("term_list")
    else:
        term.delete()
        messages.success(request, "term successfully deleted")
    return redirect("term_list")
