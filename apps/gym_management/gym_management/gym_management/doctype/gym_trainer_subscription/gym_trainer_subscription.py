import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, flt, getdate


class GymTrainerSubscription(Document):
    def validate(self):
        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("End Date cannot be before Start Date."))

        self.set_amount()
        self.check_overlap()

    def set_amount(self):
        fee = flt(frappe.db.get_value("Gym Trainer", self.trainer, "monthly_fee"))
        days = date_diff(self.end_date, self.start_date) + 1
        self.amount = flt(fee * days / 30, 2)

    def check_overlap(self):
        overlap = frappe.db.exists(
            "Gym Trainer Subscription",
            {
                "member": self.member,
                "docstatus": 1,
                "status": "Active",
                "name": ["!=", self.name],
                "start_date": ["<=", self.end_date],
                "end_date": [">=", self.start_date],
            },
        )
        if overlap:
            frappe.throw(
                _("Member already has an active trainer subscription ({0}) in this period.").format(overlap)
            )

    def on_cancel(self):
        self.db_set("status", "Cancelled")
