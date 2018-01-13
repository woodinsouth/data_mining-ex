class apriori(object):
	def __init__(self, file, min_support):
		print("----------------------------------------------------")
		print ("the frequent itemsets with " + str(min_support) + " min support are:")
		self.min_support = min_support
		self.data = self.load_data(file)
		self.frequent_itemset(self.data, self.min_support)
		print("----------------------------------------------------")

	def load_data(self, file):
		with open(file, 'r') as f:
			data = []
			for transaction in f:
				transaction_list = []
				for item in transaction.split():
					transaction_list.append(item)
				data.append(transaction_list)
		return data

	'''
    gen - generate candidates
    validate - validate candidates
    '''
	def frequent_itemset(self, data, min_support):
		# scan to get 1 itemset candidate
		transaction_list, candidate_set = self.scan(data) 
		# vadiate to get 1 frequent itemset
		current_set = self.validate(transaction_list, candidate_set, min_support) 
		self.print_set(current_set)

		# generate k candidate sets and vadiated sets while set is not none
		k = 2
		while(current_set != set([])):
			candidate_set = self.gen(current_set, k)
			current_set = self.validate(transaction_list, candidate_set, min_support)
			k = k+1
			self.print_set(current_set)

	# scan to generate transaction list, 1 itemset
	def scan(self, data):
		transaction_list = []
		item_set = set()
		for transaction in data:
			transaction_prime = set()
			for item in transaction:
				item = ord(item)-65 # convert character to integer
				item_set.add(frozenset([item]))
				transaction_prime.add(item) 
			transaction_list.append(frozenset(transaction_prime))
		return transaction_list, item_set

	# validate the candidate set by selecting those frequency >= min_supposet
	def validate(self, transaction_list, candidate_set, min_support):
		current_set = set()
		for candidate in candidate_set:
			count = 0
			for transaction in transaction_list:
				if candidate.issubset(transaction):
					count = count + 1
			if float(count/len(transaction_list)) >= min_support:
				current_set.add(frozenset(candidate))
		return current_set

	# generate the candidate set by selection the joining result
	def gen(self, current_set, k):
		return set([i.union(j) for i in current_set for j in current_set if len(i.union(j)) == k])

	# print frequent items
	def print_set(self, current_set):
		for itemset in current_set:
			for item in itemset:
				print(chr(item+65) + ' ', end="")
			print (" ")

if __name__ == '__main__':
	# file_process(file)
	data = np.loadtxt("apriori_d.txt", dtype=str, delimiter='\n')
	min_support = 0.6
	apriori(data, min_support)