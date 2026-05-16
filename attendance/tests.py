from datetime import date, datetime, time
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import AttendanceRecord, BreakRecord, CompanyPolicy, EmployeeShift


class BreakRecordTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.employee = user_model.objects.create_user(
            username='employee',
            password='password123',
            first_name='Test',
            last_name='Employee',
            department='Engineering',
        )

    def test_working_hours_subtract_default_break(self):
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(9, 30),
            check_out_time=time(18, 30),
        )

        self.assertEqual(record.total_break_hours, 1.0)
        self.assertEqual(record.calculate_working_hours(), 8.0)

    def test_manual_break_does_not_double_count_default_break_overlap(self):
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(9, 30),
            check_out_time=time(18, 30),
        )
        BreakRecord.objects.create(
            attendance=record,
            break_start=time(13, 0),
            break_end=time(13, 45),
        )

        self.assertEqual(record.total_break_hours, 1.0)
        self.assertEqual(record.calculate_working_hours(), 8.0)

    def test_default_break_only_counts_overlap_with_work_session(self):
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(13, 30),
            check_out_time=time(18, 30),
        )

        self.assertEqual(record.total_break_hours, 0.5)
        self.assertEqual(record.calculate_working_hours(), 4.5)

    def test_checkout_is_blocked_during_active_break(self):
        self.client.force_login(self.employee)
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(9, 30),
        )
        BreakRecord.objects.create(attendance=record, break_start=time(13, 0))

        response = self.client.post(reverse('attendance:check_out'), follow=True)

        record.refresh_from_db()
        self.assertRedirects(response, reverse('attendance:dashboard'))
        self.assertIsNone(record.check_out_time)
        self.assertContains(response, 'Please end your active break before checking out.')

    def test_checkout_message_formats_minutes_for_short_session(self):
        self.client.force_login(self.employee)
        AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(12, 38),
        )

        checkout_at = timezone.make_aware(datetime(2026, 5, 16, 12, 47))
        with patch('attendance.views.timezone.now', return_value=checkout_at):
            response = self.client.post(reverse('attendance:check_out'), follow=True)

        self.assertContains(response, 'Total working time: 9 min.')
        self.assertNotContains(response, '0.15 hours')

    def test_company_policy_controls_default_break_window(self):
        CompanyPolicy.objects.create(
            name='Custom Break',
            default_break_start_time=time(12, 0),
            default_break_end_time=time(12, 30),
        )
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(9, 30),
            check_out_time=time(18, 30),
        )

        self.assertEqual(record.total_break_hours, 0.5)
        self.assertEqual(record.calculate_working_hours(), 8.5)

    def test_company_policy_controls_late_threshold(self):
        CompanyPolicy.objects.create(
            name='Early Late Threshold',
            office_start_time=time(9, 0),
            late_threshold_time=time(9, 15),
        )
        self.client.force_login(self.employee)

        with patch('attendance.views.is_office_ip', return_value=True), \
                patch('attendance.views.timezone.localdate', return_value=date(2026, 5, 16)), \
                patch('attendance.views.timezone.localtime', return_value=datetime(2026, 5, 16, 9, 20)):
            self.client.post(reverse('attendance:check_in'))

        record = AttendanceRecord.objects.get(employee=self.employee, date=date(2026, 5, 16))
        self.assertEqual(record.attendance_status, 'late')

    def test_employee_shift_overrides_policy_late_threshold(self):
        CompanyPolicy.objects.create(
            name='Default Policy',
            office_start_time=time(9, 30),
            late_threshold_time=time(10, 0),
        )
        EmployeeShift.objects.create(
            employee=self.employee,
            name='Early Shift',
            start_time=time(8, 0),
            end_time=time(16, 0),
            required_working_hours=7.5,
            grace_minutes=10,
        )
        self.client.force_login(self.employee)

        with patch('attendance.views.is_office_ip', return_value=True), \
                patch('attendance.views.timezone.localdate', return_value=date(2026, 5, 16)), \
                patch('attendance.views.timezone.localtime', return_value=datetime(2026, 5, 16, 8, 15)):
            self.client.post(reverse('attendance:check_in'))

        record = AttendanceRecord.objects.get(employee=self.employee, date=date(2026, 5, 16))
        self.assertEqual(record.attendance_status, 'late')
        self.assertEqual(record.expected_working_hours, 7.5)

    def test_employee_shift_required_hours_falls_back_to_policy(self):
        CompanyPolicy.objects.create(name='Default Policy', daily_working_hours=8)
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=date(2026, 5, 16),
            check_in_time=time(9, 30),
        )

        self.assertEqual(record.expected_working_hours, 8)

# Create your tests here.
