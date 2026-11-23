import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": _("Class"), "fieldname": "gym_class", "fieldtype": "Link", "options": "Gym Class", "width": 200},
        {"label": _("Total Bookings"), "fieldname": "bookings", "fieldtype": "Int", "width": 130},
        {"label": _("Attended"), "fieldname": "attended", "fieldtype": "Int", "width": 110},
    ]

    conditions = "docstatus = 1"
    values = {}
    if filters.get("from_date"):
        conditions += " AND class_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND class_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    data = frappe.db.sql(
        f"""
        SELECT gym_class, COUNT(*) AS bookings, SUM(IFNULL(attended, 0)) AS attended
        FROM `tabGym Class Booking`
        WHERE {conditions}
        GROUP BY gym_class
        ORDER BY bookings DESC
        """,
        values,
        as_dict=True,
    )

    chart = {
        "data": {
            "labels": [d.gym_class for d in data],
            "datasets": [{"name": _("Bookings"), "values": [d.bookings for d in data]}],
        },
        "type": "bar",
    }
    return columns, data, None, chart
