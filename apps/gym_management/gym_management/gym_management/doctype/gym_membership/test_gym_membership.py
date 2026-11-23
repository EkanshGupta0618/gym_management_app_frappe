import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, nowdate


def make_member():
    return frappe.get_doc({
        "doctype": "Gym Member", "member_name": "Test User",
        "email": f"test{frappe.generate_hash(length=5)}@example.com",
    }).insert()


def make_type():
    if not frappe.db.exists("Gym Membership Type", "Test Monthly"):
        frappe.get_doc({"doctype": "Gym Membership Type", "type_name": "Test Monthly",
                        "duration_days": 30, "price": 1000}).insert()
    return "Test Monthly"


class TestGymMembership(FrappeTestCase):
    def test_end_date_and_amount(self):
        m = frappe.get_doc({"doctype": "Gym Membership", "member": make_member().name,
                            "membership_type": make_type(), "start_date": nowdate()}).insert()
        self.assertEqual(str(m.end_date), str(add_days(nowdate(), 29)))
        self.assertEqual(m.amount, 1000)

    def test_overlap_blocked(self):
        member = make_member().name
        frappe.get_doc({"doctype": "Gym Membership", "member": member,
                        "membership_type": make_type(), "start_date": nowdate()}).insert().submit()
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({"doctype": "Gym Membership", "member": member,
                            "membership_type": make_type(), "start_date": nowdate()}).insert()
