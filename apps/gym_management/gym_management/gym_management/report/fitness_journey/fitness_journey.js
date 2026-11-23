frappe.query_reports["Fitness Journey"] = {
    filters: [
        {
            fieldname: "member",
            label: __("Member"),
            fieldtype: "Link",
            options: "Gym Member",
            reqd: 1,
        },
    ],
};
