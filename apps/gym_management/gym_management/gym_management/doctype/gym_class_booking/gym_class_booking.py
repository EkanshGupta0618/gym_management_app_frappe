import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class GymClassBooking(Document):
    def validate(self):
        self.check_membership()
        self.check_duplicate()
        self.check_capacity()

    def check_membership(self):
        active = frappe.db.exists(
            "Gym Membership",
            {
                "member": self.member,
                "docstatus": 1,
                "status": "Active",
                "start_date": ["<=", self.class_date],
                "end_date": [">=", self.class_date],
            },
        )
        if not active:
            frappe.throw(_("Member needs an active membership on {0} to book a class.").format(self.class_date))

    def check_duplicate(self):
        dup = frappe.db.exists(
            "Gym Class Booking",
            {
                "member": self.member,
                "gym_class": self.gym_class,
                "class_date": self.class_date,
                "docstatus": ["!=", 2],
                "name": ["!=", self.name],
            },
        )
        if dup:
            frappe.throw(_("Member already booked this class on {0} ({1}).").format(self.class_date, dup))

    def check_capacity(self):
        capacity = frappe.db.get_value("Gym Class", self.gym_class, "max_capacity") or 0
        if not capacity:
            return
        booked = frappe.db.count(
            "Gym Class Booking",
            {
                "gym_class": self.gym_class,
                "class_date": self.class_date,
                "docstatus": ["!=", 2],
                "name": ["!=", self.name],
            },
        )
        if booked >= capacity:
            frappe.throw(_("Class is full ({0}/{0}) on {1}.").format(capacity, self.class_date))
