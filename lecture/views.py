from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from lecture.forms import CourseForm, NoticeForm
from lecture.models import Course, Enrollment, Notice


def index(request):
    # TODO
    user = request.user
    context = {}
    if check_role(user) == "교수":
        # 교수
        my_courses = get_professors_courses(user)
        context["my_courses"] = my_courses

        return render(request, 'lecture/index_professor.html', context)
    elif check_role(user) == "학생":

        # get course list
        my_courses = get_students_courses(user)
        dummy_lecture_list = []

    else:
        message = 'unknown'
        my_courses = []


def get_available_course_list(request):
    user = request.user
    context = {}
    if check_role(user) == "교수":
        messages.error(request, "권한이 없습니다.")
        return render(request, 'global/error_page.html', context=context)


def course_index(request, course_id):
    context = {}
    user = request.user
    course = get_object_or_404(Course, pk=course_id)

    if check_role(user) == "교수":
        context["course"] = course
        try:
            notices = Notice.objects.all().filter(course=course)
            notices = notices.order_by('-pub_dt')[:3]
        except Notice.DoesNotExist:
            notices = []
        context["notices"] = notices

        return render(request, 'lecture/course_index.html', context=context)
    return render(request, 'global/error_page.html', context=context)


def course_create(request):
    context = {}
    user = request.user
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.professor = user
            course.save()
            return redirect('lecture:course_index', course.id)
    else:
        course_form = CourseForm()
        context['course_form'] = course_form
        return render(request, 'lecture/course_create.html', context)


def course_join(request, course_id):
    pass


def notice_index(request, course_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course
    user = request.user
    notices = Notice.objects.all().filter(course=course)
    context['notices'] = notices

    return render(request, 'lecture/notice_index.html', context)


def notice_create(request, course_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course
    notices = Notice.objects.all().filter(course=course)
    context['notices'] = notices
    user = request.user
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
        return render(request, 'lecture/notice_create.html', context)

    return None


def notice_read(request, course_id, notice_id):
    context = {}

    course = get_object_or_404(Course, id=course_id)
    notice = get_object_or_404(Notice, id=notice_id)

    context["course"] = course
    context["notice"] = notice

    return render(request, 'lecture/notice_read.html', context=context)


def notice_update(request, course_id, notice_id):
    context = {}

    course = get_object_or_404(Course, id=course_id)
    notice = get_object_or_404(Notice, id=notice_id)

    if request.user.id is not notice.publisher.id:
        return redirect('lecture:notice_read', course_id, notice_id)

    context["course"] = course
    context["notice"] = notice

    return render(request, 'lecture/notice_update.html', context=context)


def notice_comment_list(request, course_id, notice_id):
    return None


def check_if_authenticated(request):
    if request.user.is_authenticated is False:
        messages.error(request, "로그인 하셔야 합니다.")
        context = {}
        return render(request, 'global/error_page.html', context=context)


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
