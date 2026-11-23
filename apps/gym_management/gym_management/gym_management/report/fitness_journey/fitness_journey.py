import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": _("Date"), "fieldname": "log_date", "fieldtype": "Date", "width": 110},
        {"label": _("Weight (kg)"), "fieldname": "weight", "fieldtype": "Float", "width": 110},
        {"label": _("Calories"), "fieldname": "calories", "fieldtype": "Int", "width": 100},
        {"label": _("Body Fat %"), "fieldname": "body_fat", "fieldtype": "Percent", "width": 100},
        {"label": _("Notes"), "fieldname": "notes", "fieldtype": "Data", "width": 250},
    ]

    if not filters.get("member"):
        return columns, [], _("Select a member to see the fitness journey."), None

    data = frappe.get_all(
        "Gym Fitness Log",
        filters={"member": filters["member"]},
        fields=["log_date", "weight", "calories", "body_fat", "notes"],
        order_by="log_date asc",
    )

    chart = {
        "data": {
            "labels": [str(d.log_date) for d in data],
            "datasets": [
                {"name": _("Weight (kg)"), "values": [d.weight or 0 for d in data]},
                {"name": _("Calories"), "values": [d.calories or 0 for d in data]},
            ],
        },
        "type": "line",
    }
    return columns, data, None, chart
