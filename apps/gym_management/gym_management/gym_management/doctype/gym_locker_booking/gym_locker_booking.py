import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class GymLockerBooking(Document):
    def validate(self):
        self.check_locker_available()
        self.check_active_membership()
        self.check_double_booking()

    def check_locker_available(self):
        status = frappe.db.get_value("Gym Locker", self.locker, "status")
        if status == "Maintenance":
            frappe.throw(_("Locker {0} is under maintenance.").format(self.locker))

    def check_active_membership(self):
        active = frappe.db.exists(
            "Gym Membership",
            {
                "member": self.member,
                "docstatus": 1,
                "status": "Active",
                "start_date": ["<=", self.booking_date],
                "end_date": [">=", self.booking_date],
            },
        )
        if not active:
            frappe.throw(_("Member needs an active membership to book a locker."))

    def check_double_booking(self):
        if getdate(self.booking_date) < getdate(nowdate()):
            frappe.throw(_("Booking date cannot be in the past."))

        clash = frappe.db.sql(
            """
            SELECT name FROM `tabGym Locker Booking`
            WHERE locker = %(locker)s
              AND booking_date = %(date)s
              AND docstatus = 1
              AND name != %(name)s
              AND IFNULL(start_time, '00:00:00') < %(end)s
              AND IFNULL(end_time, '23:59:59') > %(start)s
            """,
            {
                "locker": self.locker,
                "date": self.booking_date,
                "name": self.name or "",
                "start": self.start_time or "00:00:00",
                "end": self.end_time or "23:59:59",
            },
        )
        if clash:
            frappe.throw(
                _("Locker {0} is already booked in that time slot ({1}).").format(
                    self.locker, frappe.bold(clash[0][0])
                )
            )
