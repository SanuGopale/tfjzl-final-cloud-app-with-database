from .models import Course, Enrollment, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if not request.user.is_authenticated:
        return redirect("onlinecourse:login")

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    if request.method == "POST":
        submission = Submission.objects.create(
            enrollment=enrollment
        )

        selected_choices = extract_answers(request)

        for choice_id in selected_choices:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)

        return redirect(
            "onlinecourse:show_exam_result",
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect(
        "onlinecourse:course_details",
        course_id=course.id
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course
    )

    selected_choices = submission.choices.all()
    total_score = 0

    for choice in selected_choices:
        if choice.is_correct:
            total_score += choice.question.grade

    context = {
        "course": course,
        "submission": submission,
        "selected_ids": selected_choices,
        "grade": total_score,
    }

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context
    )
