import frappe
from frappe.utils import date_diff, nowdate

no_cache = 1


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw("Please login to view your profile", frappe.PermissionError)

    member = frappe.db.get_value("Gym Member", {"user": frappe.session.user}, ["name", "member_name"], as_dict=True)
    context.member = member
    if not member:
        return

    memberships = frappe.get_all(
        "Gym Membership",
        filters={"member": member.name, "docstatus": 1},
        fields=["name", "membership_type", "start_date", "end_date", "status"],
        order_by="start_date desc",
    )
    today = nowdate()
    context.active = next((m for m in memberships if str(m.start_date) <= today <= str(m.end_date) and m.status == "Active"), None)
    if context.active:
        context.days_left = date_diff(context.active.end_date, today)
    context.past = [m for m in memberships if m != context.active]

    context.trainer = None
    sub = frappe.db.get_value(
        "Gym Trainer Subscription",
        {"member": member.name, "docstatus": 1, "status": "Active", "end_date": [">=", today]},
        "trainer",
    )
    if sub:
        context.trainer = frappe.db.get_value("Gym Trainer", sub, ["trainer_name", "email", "phone"], as_dict=True)
