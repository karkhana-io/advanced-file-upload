import frappe
from frappe.utils.file_manager import add_attachments, save_url
from frappe import _, is_whitelisted
from frappe.utils import cint

def test():
	print("test")

@frappe.whitelist(allow_guest=True)
def upload_file():
	settings = frappe.get_doc('Advanced File Upload Settings')
	if not settings.enabled:
		frappe.throw("Not Enabled. Contact System Administrator")

	allowed_filetypes = tuple([mimetype.extension for mimetype in settings.file_types_allowed])
	# print(doubled_odds)
	# ALLOWED_MIMETYPES = 

	user = None
	if frappe.session.user == 'Guest':
		if frappe.get_system_settings('allow_guests_to_upload_files'):
			ignore_permissions = True
		else:
			return
	else:
		user = frappe.get_doc("User", frappe.session.user)
		ignore_permissions = False

	files = frappe.request.files
	is_private = frappe.form_dict.is_private
	doctype = frappe.form_dict.doctype
	docname = frappe.form_dict.docname
	fieldname = frappe.form_dict.fieldname
	file_url = frappe.form_dict.file_url
	folder = frappe.form_dict.folder or 'Home'
	method = frappe.form_dict.method
	filename = frappe.form_dict.file_name
	content = None

	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename

	frappe.local.uploaded_file = content
	frappe.local.uploaded_filename = filename

	# if not file_url and (frappe.session.user == "Guest" or (user and not user.has_desk_access())):
	if not filename.lower().endswith(allowed_filetypes):
		frappe.throw(_("Not allowed to upload "))

	if method:
		method = frappe.get_attr(method)
		is_whitelisted(method)
		return method()
	else:
		ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
			"attached_to_field": fieldname,
			"folder": folder,
			"file_name": filename,
			"file_url": file_url,
			"is_private": cint(is_private),
			"content": content
		})
		ret.save(ignore_permissions=ignore_permissions)
		return ret
