from django.urls import path
from . import views

urlpatterns = [

    # ── Auth ──────────────────────────────────────────────────────────────
    path('', views.login_page, name='login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('student-login/', views.student_login, name='student_login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('teacher-forgot-password/', views.teacher_forgot_password, name='teacher_forgot_password'),
    path('logout/', views.logout_view, name='logout'),

    # ── Dashboards ────────────────────────────────────────────────────────
    path('dashboard/', views.home, name='home'),
    path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('student-calendar-data/', views.student_calendar_data, name='student_calendar_data'),
    path('student-timetable/', views.student_timetable, name='student_timetable'),

    # ── Legacy Redirects ──────────────────────────────────────────────────
    path('holidays/', views.legacy_holidays_redirect, name='holidays_legacy'),
    path('bulk-add-holidays/', views.legacy_holidays_redirect, name='bulk_add_holidays_legacy'),
    path('add-holiday/', views.legacy_holidays_redirect, name='add_holiday_legacy'),
    path('delete-holiday/<int:id>/', views.legacy_holidays_redirect, name='delete_holiday_legacy'),

    # ── Student Management ────────────────────────────────────────────────
    path('students/', views.students, name='students'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

    # ── Bulk Import & Registration ───────────────────────────────────────
    path('bulk-import/', views.bulk_import_students, name='bulk_import_students'),
    path('register/', views.student_register, name='student_register'),

    # ── Teacher Management ────────────────────────────────────────────────
    path('teachers/', views.teachers, name='teachers'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('edit-teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),

    # ── Class / Subject Management ────────────────────────────────────────
    path('classes/', views.classes, name='classes'),
    path('add-class/', views.add_class, name='add_class'),
    path('delete-class/<int:id>/', views.delete_class, name='delete_class'),
    path('subjects/', views.subjects, name='subjects'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('delete-subject/<int:id>/', views.delete_subject, name='delete_subject'),

    # ── Attendance ────────────────────────────────────────────────────────
    path('mark/', views.mark_page, name='mark_page'),
    path('mark/<int:student_id>/<str:status>/', views.mark_attendance, name='mark_attendance'),
    path('bulk-present/', views.bulk_mark_present, name='bulk_mark_present'),
    path('edit-attendance/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),

    # ── Reports ───────────────────────────────────────────────────────────
    path('report/', views.report, name='report'),
    path('download-excel/', views.download_excel, name='download_excel'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('send-alerts/', views.send_low_attendance_emails, name='send_alerts'),

    # ── Leave Requests ────────────────────────────────────────────────────
    path('leaves/', views.leaves, name='leaves'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('teacher-apply-leave/', views.teacher_apply_leave, name='teacher_apply_leave'),
    path('my-leaves/', views.my_leaves, name='my_leaves'),
    path('teacher-my-leaves/', views.teacher_my_leaves, name='teacher_my_leaves'),
    path('review-leave/<int:id>/<str:action>/', views.review_leave, name='review_leave'),

    # ── Notifications ─────────────────────────────────────────────────────
    path('notifications/', views.notifications, name='notifications'),
    path('mark-notification-read/<int:id>/', views.mark_notification_read, name='mark_notification_read'),

    # ── Activity Logs ─────────────────────────────────────────────────────
    path('activity-logs/', views.activity_logs, name='activity_logs'),

    # ── Timetable ─────────────────────────────────────────────────────────
    path('timetable/', views.timetable, name='timetable'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('delete-timetable/<int:id>/', views.delete_timetable, name='delete_timetable'),

    # ── Admin Panel ───────────────────────────────────────────────────────
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
