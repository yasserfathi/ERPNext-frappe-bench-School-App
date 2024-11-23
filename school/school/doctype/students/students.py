# Copyright (c) 2024, Yasser Ibrahim and contributors
# For license information, please see license.txt

import frappe
import csv
from csv import writer
import os.path
from frappe.model.document import Document

class Students(Document):
	DATA_FILE = "data.csv"

	def before_save(self):
		self.full_name = f"{self.first_name} {self.second_name}"
	
	@staticmethod
	def read_data_from_csv_file():
		curr_path = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(curr_path, Students.DATA_FILE)
		dict = []
		with open(file_path) as csvfile:
			reader = csv.DictReader(csvfile,delimiter=',')
			for row in reader:
				dict.append(row)
		return dict
	
	def update_data(self, data: dict[str, dict]) -> None:
		curr_path = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(curr_path, Students.DATA_FILE)
		with open(file_path, 'w', newline='') as csvfile:
			fieldnames = ['name', 'first_name', 'second_name', 'birth_date', 'country']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerows(data)
		
	def db_insert(self, *args, **kwargs):
		d = self.get_valid_dict(convert_dates_to_str=True)
		curr_path = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(curr_path, Students.DATA_FILE)
		with open(file_path, 'a') as f_object:
			# Pass this file object to csv.writer()
			# and get a writer object
			writer_object = writer(f_object)
		
			# Pass the list as an argument into
			# the writerow()
			writer_object.writerow([d.full_name,d.first_name,d.second_name,d.birth_date,d.country])
		
			# Close the file object
			f_object.close()
		frappe.msgprint('Successfully Added')
	
	def load_from_db(self):
		item_dict = []
		data = self.read_data_from_csv_file()
		for item in data:
			if self.name == item['name']:
				item_dict = item	
		super(Document, self).__init__(item_dict)
		
	def db_update(self):
		pass

	@staticmethod
	def get_list(args):
		data = Students.read_data_from_csv_file()
		return data


	@staticmethod
	def get_count(args):
		data = Students.read_data_from_csv_file()
		return len(data)

	@staticmethod
	def get_stats(args):
		pass
	
	def delete(self):
		frappe.msgprint(len(self))
		
		curr_path = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(curr_path, Students.DATA_FILE)
		dict = []
		with open(file_path) as csvfile:
			reader = csv.DictReader(csvfile,delimiter=',')
			for row in reader:
				if row['name'] != self.name:
					dict.append(row)
		self.update_data(dict)

