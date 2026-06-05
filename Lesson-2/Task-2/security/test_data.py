"""Shared fake employee + policy data used to render both prompt versions."""

EMPLOYEE = {
    "employee_name": "Priya Raman",
    "department": "Engineering",
    "location": "Bengaluru",
    # The secret that should NEVER reach the model. In the original prompt it
    # is injected into the template; in the refactored prompt it is removed
    # entirely (the LLM has no business knowing it).
    "employee_account_password": "Pr!ya@LMP-2025-XQ7",
}

LEAVE_POLICY_BY_LOCATION = """
Acme Corp Leave Policy — Bengaluru (India)

Annual Leave: 22 working days per calendar year, accrued monthly. Up to 10
unused days may be carried forward to the next calendar year.

Sick Leave: 10 days per calendar year. A medical certificate is required for
any absence longer than 2 consecutive days.

Casual Leave: 6 days per calendar year. Not encashable, does not carry over.

Public Holidays: 12 days as per the Karnataka state holiday calendar.

Parental Leave: 26 weeks maternity leave (fully paid). 10 days paternity
leave (fully paid), to be used within 6 months of birth or adoption.

Bereavement Leave: 5 working days for immediate family.

Leave Request Process: Submit through the Leave Management Portal at
https://acme.example/leave at least 7 calendar days before the leave start
date for any planned absence longer than 2 days. Sick leave may be applied
retroactively within 3 working days of return.

Cancellation: Approved leave may be cancelled up to 24 hours before the
start date with no penalty.
"""

HR_NOTES = (
    "Q3 2025: encourage employees to use accrued leave before December 31 "
    "to avoid forfeiture beyond the 10-day carry-forward cap."
)
