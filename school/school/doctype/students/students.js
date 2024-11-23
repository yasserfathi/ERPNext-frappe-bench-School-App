// Copyright (c) 2024, Yasser Ibrahim and contributors
// For license information, please see license.txt

frappe.ui.form.on("Students", {
	validate(frm) {
        if(frm.doc.birth_date < frappe.datetime.nowdate()) {
            frappe.throw(__('You can not select past date in From Date'));
            f1  = document.querySelector('[data-doctype="Items"][data-fieldname="birth_date"]');
	        f1.style.border="solid 1px green";
        }
	},
});