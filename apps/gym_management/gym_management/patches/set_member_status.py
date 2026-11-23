import frappe


def execute():
    frappe.db.sql(
        """UPDATE `tabGym Member` SET status = 'Active'
           WHERE status IS NULL OR status = ''"""
    )
