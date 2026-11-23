import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate


class GymMembership(Document):
    def validate(self):
        self.set_end_date_and_amount()
        self.check_overlap()

    def set_end_date_and_amount(self):
        mtype = frappe.db.get_value(
            "Gym Membership Type", self.membership_type,
            ["duration_days", "price"], as_dict=True,
        )
        if not mtype:
            frappe.throw(_("Invalid Membership Type"))

        self.end_date = add_days(getdate(self.start_date), mtype.duration_days - 1)
        self.amount = mtype.price

    def check_overlap(self):
        overlap = frappe.db.sql(
            """
            SELECT name FROM `tabGym Membership`
            WHERE member = %(member)s
              AND docstatus = 1
              AND status = 'Active'
              AND name != %(name)s
              AND start_date <= %(end)s
              AND end_date >= %(start)s
            """,
            {
                "member": self.member,
                "name": self.name or "",
                "start": self.start_date,
                "end": self.end_date,
            },
        )
        if overlap:
            frappe.throw(
                _("Member already has an active membership {0} overlapping these dates.").format(
                    frappe.bold(overlap[0][0])
                )
            )

    def on_submit(self):
        frappe.db.set_value("Gym Member", self.member, "status", "Active")

    def on_cancel(self):
        self.db_set("status", "Cancelled")
