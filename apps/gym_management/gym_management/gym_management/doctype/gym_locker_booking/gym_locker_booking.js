frappe.ui.form.on("Gym Locker Booking", {
    setup(frm) {
        frm.set_query("locker", () => ({
            filters: { status: ["!=", "Maintenance"] },
        }));
    },
});
