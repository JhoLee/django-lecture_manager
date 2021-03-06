from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from lecture.forms import CourseForm, NoticeForm, NoticeCommentForm
from lecture.models import Course, Enrollment, Notice, NoticeComment


def index(request):
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    context = {}
    if check_role(user) == "교수":
        # 교수
        my_courses = get_professors_courses(user)
        context["my_courses"] = my_courses

        context['course_count'] = len(my_courses)

        return render(request, 'lecture/index_professor.html', context)
    elif check_role(user) == "학생":

        # get course list
        my_courses = get_students_courses(user)

        course_count = len(my_courses)
        context["my_courses"] = my_courses
        context["course_count"] = course_count

        return render(request, 'lecture/index_student.html', context)

    else:
        message = 'unknown'
        my_courses = []


def course_index(request, course_id):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    course = get_object_or_404(Course, pk=course_id)
    context["course"] = course

    if check_role(user) == "학생":
        enrollment = Enrollment.objects.filter(course=course)
        if not enrollment.filter(student=user).exists():
            return redirect('lecture:course_join', course_id)

    if check_role(user) == "교수" and course.professor.id is not user.id:
        return redirect('lecture:index')
    try:
        notices = Notice.objects.all().filter(course=course)
        notices = notices.order_by('-pub_dt')[:3]
    except Notice.DoesNotExist:
        notices = []
    context["notices"] = notices

    return render(request, 'lecture/course/course_index.html', context=context)


def course_create(request):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.professor = user
            course.save()
            return redirect('lecture:course_index', course.id)
        else:
            messages.error(request, "무언가 잘못 되었습니다. 다시 시도해주세요.")
            context['course_form'] = course_form
    else:
        course_form = CourseForm()
        context['course_form'] = course_form
    return render(request, 'lecture/course/course_create.html', context)


def course_update(request, course_id):
    context = {}

    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')

    if request.user.id is not course.professor.id:
        return redirect('lecture:course_index', course_id)

    context['course'] = course
    context['user'] = user

    if request.method == "POST":
        course_form = CourseForm(request.POST or None, instance=course)

        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.professor = user
            new_course.save()

            messages.info(request, "강의 수정 완료!")

            return redirect('lecture:course_index', course.id)
    else:
        course_form = CourseForm(instance=course)

    context['course_form'] = course_form
    return render(request, 'lecture/course/course_update.html', context)


def course_delete(request, course_id):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    course = get_object_or_404(Course, id=course_id)

    if request.user.id is not course.professor.id:
        return redirect('lecture:course_index', course_id)

    course.delete()
    messages.info(request, "강의 삭제 완료!")
    return redirect('lecture:index')


def course_join(request, course_id):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')

    if check_role(user) == "교수":
        messages.error(request, "권한이 없습니다.")
        return redirect('lecture:index')
    is_enrolled = Enrollment.objects.filter(student=user, course=course_id).exists()
    if is_enrolled:
        context['is_enrolled'] = True
        return render(request, 'lecture/course/course_join.html', context)
    else:
        if request.method == "POST":
            _id = request.POST['_id']
            course = get_object_or_404(Course, pk=_id)
            Enrollment.objects.create(course=course, student=user)
            messages.info(request, '강의 참가 완료!')

            return redirect('lecture:course_index', _id)
        context['is_enrolled'] = False
        course = get_object_or_404(Course, pk=course_id)
        context['course'] = course

        return render(request, 'lecture/course/course_join.html', context)


def notice_index(request, course_id):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course
    user = request.user
    notices = Notice.objects.all().filter(course=course)

    context['notices'] = notices

    return render(request, 'lecture/notice/notice_index.html', context)


def notice_create(request, course_id):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course
    notices = Notice.objects.all().filter(course=course)
    context['notices'] = notices
    if request.method == "POST":
        notice_form = NoticeForm(request.POST, request.FILES)
        if notice_form.is_valid():
            notice = notice_form.save(commit=False)
            notice.publisher = user
            notice.course = course
            notice.save()
            return redirect('lecture:notice_index', course.id)
    else:
        notice_form = NoticeForm()
        context['notice_form'] = notice_form
        return render(request, 'lecture/notice/notice_create.html', context)


def notice_read(request, course_id, notice_id):
    context = {}

    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    course = get_object_or_404(Course, id=course_id)
    notice = get_object_or_404(Notice, id=notice_id)
    comments = get_notice_comment_list(request, course_id, notice_id)

    context["user"] = user
    context["course"] = course
    context["notice"] = notice
    context["comments"] = comments

    return render(request, 'lecture/notice/notice_read.html', context=context)


def notice_update(request, course_id, notice_id):
    context = {}

    course = get_object_or_404(Course, pk=course_id)
    notice = get_object_or_404(Notice, pk=notice_id)
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')

    if request.user.id is not notice.publisher.id:
        return redirect('lecture:notice_read', course_id, notice_id)

    context["course"] = course
    context["notice"] = notice
    context["user"] = user

    if request.method == "POST":
        notice_update_form = NoticeForm(request.POST or None, request.FILES or None, instance=notice)

        if notice_update_form.is_valid():
            new_notice = notice_update_form.save(commit=False)
            new_notice.course = course
            new_notice.publisher = request.user
            new_notice.save()

            return redirect('lecture:notice_read', course.id, new_notice.id)
    else:
        notice_update_form = NoticeForm(instance=notice)

    context["notice_update_form"] = notice_update_form

    return render(request, 'lecture/notice/notice_update.html', context=context)


def notice_delete(request, course_id, notice_id):
    context = {}
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    course = get_object_or_404(Course, id=course_id)
    notice = get_object_or_404(Notice, id=notice_id)

    if request.user.id is not notice.publisher.id:
        return redirect('lecture:notice_read', course_id, notice_id)

    notice.delete()
    messages.info(request, "게시글 삭제 완료!")
    return redirect('lecture:notice_index', course.id)


def get_notice_comment_list(request, course_id, notice_id):
    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')
    notice = get_object_or_404(Notice, id=notice_id)
    comments = NoticeComment.objects.all().filter(notice=notice)

    return comments


def notice_comment_create(request, course_id, notice_id):
    context = {}

    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')

    course = get_object_or_404(Course, pk=course_id)
    notice = get_object_or_404(Notice, pk=notice_id)

    context['course'] = course
    context['notice'] = notice

    user = request.user
    if request.method == "POST":
        comment_form = NoticeCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.writer = user
            comment.notice = notice
            comment.save()
            return redirect('lecture:notice_read', course.id, notice.id)
    else:
        comment_form = NoticeCommentForm()
        context['comment_form'] = comment_form
        return render(request, 'lecture/notice/notice_comment_create.html', context)


def notice_comment_update(request, course_id, notice_id, comment_id):
    context = {}

    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')

    course = get_object_or_404(Course, id=course_id)
    notice = get_object_or_404(Notice, id=notice_id)
    comment = get_object_or_404(NoticeComment, id=comment_id)

    if request.user.id is not comment.writer.id:
        return redirect('lecture:notice_read', course_id, notice_id)

    context["course"] = course
    context["notice"] = notice
    context["comment"] = comment

    initial_data = {
        'title': comment.title,
        'content': comment.content,
        'file': comment.file,
    }
    form = NoticeCommentForm(request.POST, request.FILES, initial=initial_data, instance=comment)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = request.user
            comment.notice = notice
            comment.save()

            return redirect('lecture:notice_read', course.id, notice.id)
    else:
        form = NoticeCommentForm(instance=comment)

    context['comment_update_form'] = form
    return render(request, 'lecture/notice/notice_comment_update.html', context=context)


def notice_comment_delete(request, course_id, notice_id, comment_id):
    context = {}

    user = request.user
    if not check_if_authenticated(request):
        return redirect('accounts:login')

    course = get_object_or_404(Course, id=course_id)
    notice = get_object_or_404(Notice, id=notice_id)
    comment = get_object_or_404(NoticeComment, id=comment_id)
    comment.delete()

    return redirect('lecture:notice_read', course.id, notice_id)


def check_if_authenticated(request):
    if request.user.is_authenticated is False:
        messages.error(request, "로그인 하셔야 합니다.")
        return False
    else:
        return True


def get_students_courses(student):
    try:
        my_courses = []
        my_enrollments = Enrollment.objects.filter(
            student=student.profile.id
        )

        for enrollment in my_enrollments:
            my_courses.append(enrollment.course)
    except Enrollment.DoesNotExist:
        my_courses = []
    return my_courses


def get_professors_courses(professor):
    try:
        my_courses = Course.objects.filter(
            professor=professor.profile.id
        )
    except Course.DoesNotExist:
        my_courses = []
    return my_courses


def check_role(user):
    if user.profile.role == 0:
        return "학생"
    elif user.profile.role == 1:
        return "교수"
    else:
        return "unknown"


def course_search(request):
    context = {}

    user = request.user

    if check_role(user) == "교수":
        return redirect('lecture:index')

    available_courses = get_available_course_list(user)
    context['available_courses'] = available_courses

    return render(request, 'lecture/search_course.html', context)


def get_available_course_list(user):
    if check_role(user) == "교수":
        return None
    elif check_role(user) == "학생":
        courses = Course.objects.all()
        enroll = Enrollment.objects.all().filter(student=user)
        for en in enroll:
            courses = courses.exclude(pk=en.course.id)
        return courses
