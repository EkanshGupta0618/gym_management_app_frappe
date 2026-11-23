frappe.query_reports["Monthly Revenue"] = {
    filters: [
        {
            fieldname: "year",
            label: __("Year"),
            fieldtype: "Int",
            default: new Date().getFullYear(),
        },
    ],
};
