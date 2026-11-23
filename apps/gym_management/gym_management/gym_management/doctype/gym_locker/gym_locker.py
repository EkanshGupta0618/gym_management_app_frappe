import frappe
from frappe import _
from frappe.model.document import Document


class GymLocker(Document):
    def validate(self):
        limit = frappe.db.get_single_value("Gym Settings", "total_lockers") or 0
        count = frappe.db.count("Gym Locker", {"name": ["!=", self.name]})
        if limit and count >= limit:
            frappe.throw(
                _("Locker limit reached. Gym Settings allows only {0} lockers.").format(limit)
            )
