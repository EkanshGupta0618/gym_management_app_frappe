frappe.ui.form.on("Gym Trainer Subscription", {
    trainer: calc,
    start_date: calc,
    end_date: calc,
});

function calc(frm) {
    if (!frm.doc.trainer || !frm.doc.start_date || !frm.doc.end_date) return;
    frappe.db.get_value("Gym Trainer", frm.doc.trainer, "monthly_fee").then(({ message }) => {
        const days = frappe.datetime.get_diff(frm.doc.end_date, frm.doc.start_date) + 1;
        if (days < 1) return;
        frm.set_value("amount", flt((message.monthly_fee || 0) * days / 30, 2));
    });
}
