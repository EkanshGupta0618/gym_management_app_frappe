import frappe
from frappe.utils import add_days, nowdate, getdate


def send_weekly_class_summary():
    day = frappe.db.get_single_value("Gym Settings", "weekly_email_day") or "Sunday"
    if getdate(nowdate()).strftime("%A") != day:
        return

    start, end = add_days(nowdate(), -6), nowdate()
    rows = frappe.db.sql(
        """
        SELECT member, gym_class, class_date FROM `tabGym Class Booking`
        WHERE docstatus = 1 AND attended = 1 AND class_date BETWEEN %s AND %s
        ORDER BY class_date
        """,
        (start, end),
        as_dict=True,
    )

    by_member = {}
    for r in rows:
        by_member.setdefault(r.member, []).append(r)

    for member, items in by_member.items():
        email = frappe.db.get_value("Gym Member", member, "email")
        name = frappe.db.get_value("Gym Member", member, "member_name")
        if not email:
            continue
        lines = "".join(f"<li>{i.gym_class} on {i.class_date}</li>" for i in items)
        frappe.sendmail(
            recipients=[email],
            subject="Your weekly gym class summary",
            message=f"<p>Hi {name},</p><p>Classes you attended this week:</p><ul>{lines}</ul>",
        )
