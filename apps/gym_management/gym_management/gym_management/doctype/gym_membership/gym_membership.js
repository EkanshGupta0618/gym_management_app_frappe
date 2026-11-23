frappe.ui.form.on("Gym Membership", {
    membership_type(frm) {
        frm.trigger("calculate_dates");
    },
    start_date(frm) {
        frm.trigger("calculate_dates");
    },
    calculate_dates(frm) {
        if (!frm.doc.membership_type || !frm.doc.start_date) return;
        frappe.db
            .get_value("Gym Membership Type", frm.doc.membership_type, ["duration_days", "price"])
            .then(({ message }) => {
                frm.set_value("amount", message.price);
                frm.set_value(
                    "end_date",
                    frappe.datetime.add_days(frm.doc.start_date, message.duration_days - 1)
                );
            });
    },
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === "Active") {
            const left = frappe.datetime.get_diff(frm.doc.end_date, frappe.datetime.get_today());
            frm.dashboard.add_comment(
                left >= 0 ? __("{0} days remaining", [left]) : __("Expired"),
                left >= 0 ? "green" : "red",
                true
            );
        }
    },
});
