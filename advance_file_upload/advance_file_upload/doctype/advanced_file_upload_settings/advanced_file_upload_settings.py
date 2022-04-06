# Copyright (c) 2022, Karkhana.io and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AdvancedFileUploadSettings(Document):
	def validate(self):
		check_for_duplicate_entries(self)
		
def check_for_duplicate_entries(self):
	extension = [mimetype.extension for mimetype in self.file_types_allowed]
	if len(extension) != len(set(extension)):
		frappe.throw("Duplicate entries in extension column")
