import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 120},
        {"label": _("Memberships"), "fieldname": "membership", "fieldtype": "Currency", "width": 150},
        {"label": _("Trainer Subscriptions"), "fieldname": "trainer", "fieldtype": "Currency", "width": 180},
        {"label": _("Total"), "fieldname": "total", "fieldtype": "Currency", "width": 150},
    ]

    year_cond = ""
    values = {}
    if filters.get("year"):
        year_cond = " AND YEAR(start_date) = %(year)s"
        values["year"] = filters["year"]

    months = {}

    def collect(doctype, key):
        rows = frappe.db.sql(
            f"""
            SELECT DATE_FORMAT(start_date, '%%Y-%%m') AS month, SUM(amount) AS amt
            FROM `tab{doctype}`
            WHERE docstatus = 1 {year_cond}
            GROUP BY month
            """,
            values,
            as_dict=True,
        )
        for r in rows:
            months.setdefault(r.month, {"month": r.month, "membership": 0, "trainer": 0})
            months[r.month][key] = flt(r.amt)

    collect("Gym Membership", "membership")
    collect("Gym Trainer Subscription", "trainer")

    data = sorted(months.values(), key=lambda x: x["month"])
    for d in data:
        d["total"] = d["membership"] + d["trainer"]

    chart = {
        "data": {
            "labels": [d["month"] for d in data],
            "datasets": [
                {"name": _("Memberships"), "values": [d["membership"] for d in data]},
                {"name": _("Trainer Subscriptions"), "values": [d["trainer"] for d in data]},
            ],
        },
        "type": "bar",
        "barOptions": {"stacked": 1},
    }
    return columns, data, None, chart
