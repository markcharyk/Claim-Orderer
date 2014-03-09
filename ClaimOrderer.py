#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ClaimOrderer.py
#  
#  Copyright 2013 Mark Calkins Charyk <Mark@MARKTOSHIBA>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from operator import attrgetter
from Tkinter import *

class ClaimList(object):
	# Simply create an empty list for the ClaimList object
	def __init__(self):
		self.claims = []
	
	# Add a claim to the list
	def add_claim(self, clm):
		self.claims.append(clm)
		self.final = len(self.claims)
	
	# Get the length of the list	
	def get_length(self):
		return len(self.claims)
	
	# Return the claim of a given claim number	
	def get_claim(self, claim_number):
		for i in self.claims:
			if i.get_num() == claim_number:
				return i
		# Handle the case where there is no such claim number
		print("There is no claim numbered " + claim_number)
		return None
	
	# Cause ClaimList to be iterable through the list of claims
	def __iter__(self):
		return iter(self.claims)
		
	# Add a reference to a claim and its dependents
	def add_reference(self, clm, ref):
		self.get_claim(clm).add_ref(ref)
		for i in self.get_claim(clm).get_dependents():
			self.add_reference(i, ref)
			
	# Delete a reference from a claim and its dependents
	def delete_reference(self, clm, ref):
		self.get_claim(clm).del_ref(ref)
		for i in self.get_claim(clm).get_dependents():
			self.delete_reference(i, ref)
	
	# Assign a reference order number to each claim	
	def determine_ref_order(self):
		cnt = 0
		self.claims[0].set_ref_order(cnt)
		for i in self.claims:
			# check all former reference lists
			for j in self.claims:
				if j == i:
					# All previous claims have been checked
					cnt += 1
					i.set_ref_order(cnt)
					break
				elif j.get_refs() == i.get_refs():
					# The reference order was found in a previous claim
					i.set_ref_order(j.get_ref_order())
					break
			
	# Sort the claims into the appropriate order
	def sort_by_number(self):
		self.claims = sorted(self.claims, key=attrgetter('num'))

	def sort_by_ref_num(self):
		self.claims = sorted(self.claims, key=lambda clm: len(clm.get_refs()))

	def sort_by_ref_order(self):
		self.claims = sorted(self.claims, key=attrgetter('ref_order'))
	
			
class Claim(object):
	
	# Initialize the claim with (if appropriate) its parents' references
	def __init__(self, num, parent_claim):
		# List of the claims that depend from this claim
		self.dependents = []
		
		# List of references applying to this claim
		self.references = []

		# Check to make sure the claim is correctly numbered
		if num < 0:
			print('Claims must be numbered appropriately')
			raise Exception()
		# If the claim is not independent
		elif parent_claim is not None and parent_claim.num > 0:
			# Add the claim to the parents' list of dependents
			parent_claim.dependents.append(num)
		
		# Assign the claim its variables
		self.num = num
		self.num_refs = 0
		self.ref_order = 0
	
	# Get the claim number
	def get_num(self):
		return self.num
		
	# Get the list of references
	def get_refs(self):
		return self.references
		
	# Get the list of dependent claim numbers
	def get_dependents(self):
		return self.dependents
		
	# Add a reference to the claim's rejection
	def add_ref(self, ref):		
		for r in self.references:
			# If reference is found in the list, halt the function
			if r == ref:
				return
		# If the reference is not found, add the reference to the list		
		self.references.append(ref)
		self.num_refs += 1
		
	# Delete a reference from the claim's rejection	
	def del_ref(self, ref):
		if self.references.count(ref) == 1:
			# The reference is found in the list; remove it
			self.references.remove(ref)
			self.num_refs -= 1
		
		
	# Get the number representation of the reference order
	def get_ref_order(self):
		return self.ref_order
		
	# Determine the sorting number for the "reference order" index
	def set_ref_order(self, num):
		self.ref_order = num
		
	# Create a representation of the claim
	def __str__(self):
		rtn = "Claim " + str(self.num) + ": "
		for s in self.references:
			rtn = rtn + s + ", "
		return rtn
	
		

def main():
	# Create the ClaimList
	claim_lst = ClaimList()
	
	# Get an input for the number of claims
	leng = int(input("Enter the number of claims: "))
	for x in range(leng):
		# Input the number and the parent claim
		num = int(input("Claim number? "))
		dep_num = int(input("Parent? (If independent, use 0) "))
		
		if dep_num == 0:
			# The claim is independent
			dep = None
				
		# Search for the input parent claim		
		for y in claim_lst:
			if y.get_num() == dep_num:
				# The parent claim is found
				dep = y
				break
		
		# Add the claim to the ClaimList		
		claim_lst.add_claim(Claim(num,dep))
	
	state = str(input("Add (a), delete (d), print (p), or exit (x)? "))
	
	# Allow the user to edit/print the list until they exit the program
	while(state.lower() != 'x'):
		if state.lower() == 'a':
			# Add a reference
			imp = int(input("Claim number: "))
			clm = claim_lst.get_claim(imp)
			if clm is not None:
				# The claim is found
				add_ref = input("Reference name: ")
				claim_lst.add_reference(imp, add_ref)
				
		elif state.lower() == 'd':
			# Delete a reference
			imp = int(input("Claim number: "))
			clm = claim_lst.get_claim(imp)
			if clm is not None:
				# The claim is found
				del_ref = input("Reference name: ")
				claim_lst.delete_reference(imp, del_ref)
				
		elif state.lower() == 'p':
			# Print the claim list
			# Sort the claims
			claim_lst.sort_by_number()
			claim_lst.sort_by_ref_num()
			claim_lst.determine_ref_order()
			claim_lst.sort_by_ref_order()
		
			# Print out the order	
			for x in claim_lst:
				print(str(x))
				
		else:
			# An incorrect input was received
			print("Please enter a, d, p, or x.")
		
		state = str(input("Add (a), delete (d), print (p), or exit (x)? "))
		
	return 0

if __name__ == '__main__':
	main()

