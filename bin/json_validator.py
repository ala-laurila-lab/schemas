#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jsonschema
import json
import sys
import urllib2

class SimpleValidator(object):
	""" Defines a class to load schema from url and parse json agains it.
	Does not check anything and crashes on error so user can fix the cause :P
	
	Prints "<Filename> is valid" if succeeds
	"""
	
	def __init__(self, file_to_validate):
		""" 
		file_to_validate : path to file to open
		"""
		with open(file_to_validate, 'rb') as f:
			# file to validate
			parsed_file_to_validate = json.load(f)
			
			# get schema url and load it
			schema_url = parsed_file_to_validate['$schema']
			schema = self._load_schema_from_url(schema_url)
			
			# validate parsed file against the schema
			jsonschema.validate(parsed_file_to_validate, schema)
			
			# No error means that the file is valid
			print('%s is valid' % file_to_validate)
			
	def _load_schema_from_url(self, url):
		"""
		url : load schema from given url and parse json
		"""
		response = urllib2.urlopen(url)
		schema = response.read()
		parsed_schema = json.loads(schema)
		return parsed_schema
		
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Takes the json file to check as only parameter. Prints "<Filename> is valid" if succeeds.')
		sys.exit(0)
	
	# the class will throw exception if file is not found
	file_to_validate = sys.argv[1]
	
	try:
		SimpleValidator(file_to_validate)
	except jsonschema.exceptions.ValidationError as e:
		print(e)
	except IOError as e:
		print(e)
	