frappe.ui.form.on("Gym Class Booking", {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && !frm.doc.attended) {
            frm.add_custom_button(__("Mark Attended"), () => {
                frappe.db.set_value("Gym Class Booking", frm.doc.name, "attended", 1).then(() => frm.reload_doc());
            });
        }
    },
});
