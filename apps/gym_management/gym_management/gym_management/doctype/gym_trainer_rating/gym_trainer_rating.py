import frappe
from frappe import _
from frappe.model.document import Document


class GymTrainerRating(Document):
    def validate(self):
        self.check_subscription()
        self.check_duplicate()

    def check_subscription(self):
        subscribed = frappe.db.exists(
            "Gym Trainer Subscription",
            {"member": self.member, "trainer": self.trainer, "docstatus": 1},
        )
        if not subscribed:
            frappe.throw(_("Only members subscribed to this trainer can rate them."))

    def check_duplicate(self):
        dup = frappe.db.exists(
            "Gym Trainer Rating",
            {"member": self.member, "trainer": self.trainer, "name": ["!=", self.name]},
        )
        if dup:
            frappe.throw(_("You have already rated this trainer."))

    def on_update(self):
        update_trainer_average(self.trainer)

    def on_trash(self):
        update_trainer_average(self.trainer, exclude=self.name)


def update_trainer_average(trainer, exclude=None):
    filters = {"trainer": trainer}
    if exclude:
        filters["name"] = ["!=", exclude]
    ratings = frappe.get_all("Gym Trainer Rating", filters=filters, pluck="rating")
    avg = (sum(ratings) / len(ratings) * 5) if ratings else 0
    frappe.db.set_value("Gym Trainer", trainer, "average_rating", round(avg, 2))
