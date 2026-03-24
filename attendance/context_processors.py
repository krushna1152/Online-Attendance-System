from .models import Student, Teacher


def navbar_student(request):
    if request.session.get('role') != 'student':
        return {'navbar_student': None}

    student_id = request.session.get('student_id')
    if not student_id:
        return {'navbar_student': None}

    student = Student.objects.filter(id=student_id).only('id', 'name', 'photo').first()
    return {'navbar_student': student}


def navbar_teacher(request):
    if request.session.get('role') != 'teacher':
        return {'navbar_teacher': None}

    teacher_id = request.session.get('teacher_db_id')
    if not teacher_id:
        return {'navbar_teacher': None}

    teacher = Teacher.objects.filter(id=teacher_id).only('id', 'name', 'photo').first()
    return {'navbar_teacher': teacher}
