train_data = [
['sales','senior','31...35','46k...50k',30],
['sales','junior', '26...30','26k...30k',40],
['sales','senior','31...35','31k...35k',40],
['systems','junior','21...25','46k...50k',20],
['systems','senior','31...35','66k...70k',5],
['systems','junior','26...30','46k...50k',3],
['systems','senior','41...45','66k...70k',3],
['marketing','senior','36...40','46k...50k',10],
['marketing','junior','31...35','41k...45k',4],
['secretary','senior','46...50','36k...40k',4],
['secretary','junior','26...30','26k...30k',6]
]

test_data = ['systems','26...30','46k...50k']

header = ['department', 'status', 'age','salary','count']

class NaiveBayes(object):
	"""docstring for NaiveBayes"""
	def __init__(self, train_data, test_data):
		print("the result predicted by the naive bayes classfier: ")
		self.train_data = train_data
		self.test_data = test_data
		NB_classifier = self.NB_train(train_data)
		self.NB_test(test_data, NB_classifier)
		print("----------------------------------------------------")
	
	def NB_train(self, train_data):
		# 0 for junior, 1 for senior 
		convert_train_data = [{},{}]
		NB_classifier = [{},{}]

		for attribute_index in range(3):
			convert_train_data[0][attribute_index] = []
			convert_train_data[1][attribute_index] = []
			NB_classifier[0][attribute_index] = {}
			NB_classifier[1][attribute_index] = {}

		for train in train_data:
			for attribute_index in range(3):
				if attribute_index >= 1:
					attribute = train[attribute_index+1]
				else:
					attribute = train[attribute_index]
				if train[1] == 'junior':
					convert_train_data[0][attribute_index].append(attribute) 
				else:
					convert_train_data[1][attribute_index].append(attribute) 

		for i in range(2):
			for attribute_index in range(3):
				attribute_value_set = set(convert_train_data[i][attribute_index])
				size = len(convert_train_data[i][attribute_index])
				for attribute_value in attribute_value_set:
					NB_classifier[i][attribute_index][attribute_value]= convert_train_data[i][attribute_index].count(attribute_value)/size

		return NB_classifier

	def NB_test(self, test_data, NB_classifier):
		prob = []
		for i in range(2):
			prob.append(1)
			for attribute_index in range(3):
				attribute_value = test_data[attribute_index]
				if attribute_value in NB_classifier[i][attribute_index].keys():
					prob[i] *= NB_classifier[i][attribute_index][attribute_value]
				else:
					prob[i] *= 0.05 # smoothing
		
		if prob[1] > prob[0]:
			print ("senior")
		else:
			print ("junior")

		
class DesisionTree(object):
	"""docstring for DesisionTree"""
	def __init__(self, train_data):
		print("the decision tree built from the train data: ")
		self.train_data = train_data
		self.print_tree(self.build_tree(train_data))
		print("----------------------------------------------------")

	def build_tree(self, rows):
		#  Try partitioing the dataset on each of the unique attribute,calculate the information gain
		#  and return the question that produces the highest gain.
		gain, question = self.find_best_split(rows)
		if gain == 0:
			return Leaf(rows)

		true_rows, false_rows = self.partition(rows, question)

		# Recursively build the branch.
		true_branch = self.build_tree(true_rows)
		false_branch = self.build_tree(false_rows)

		return Decision_Node(question, true_branch, false_branch)
	
	def find_best_split(self, rows):
		best_gain = 0  
		best_question = None  
		current_uncertainty = self.gini(rows)
		n_features = len(rows[0]) - 1  

		for col in range(n_features):
			if col >= 1:
				col += 1

			values = set([row[col] for row in rows])  # unique values in the column

			for val in values:
				question = Question(col, val)
				true_rows, false_rows = self.partition(rows, question)
				if len(true_rows) == 0 or len(false_rows) == 0:
					continue

				gain = self.info_gain(true_rows, false_rows, current_uncertainty)

				if gain >= best_gain:
					best_gain, best_question = gain, question

		return best_gain, best_question

	def gini(self, rows):
		counts = self.class_counts(rows)
		impurity = 1
		for lbl in counts:
			prob_of_lbl = counts[lbl] / float(len(rows))
			impurity -= prob_of_lbl**2
		return impurity

	def partition(self, rows, question):
		true_rows, false_rows = [], []
		for row in rows:
			if question.match(row):
				true_rows.append(row)
			else:
				false_rows.append(row)
		return true_rows, false_rows

	def info_gain(self, left, right, current_uncertainty):
		p = float(len(left)) / (len(left) + len(right))
		return current_uncertainty - p * self.gini(left) - (1 - p) * self.gini(right)

	def class_counts(self, rows):
		counts = {}
		for row in rows:
			label = row[1]
			if label not in counts:
				counts[label] = 0
			counts[label] += 1
		return counts

	def print_tree(self, node, spacing=""):
		if isinstance(node, Leaf):
			print (spacing + "Predict", node.predictions)
			return

		# Print the question at this node
		print (spacing + str(node.question))

		# Call this function recursively on the true branch
		print (spacing + '--> True:')
		self.print_tree(node.true_branch, spacing + "  ")

        # Call this function recursively on the false branch
		print (spacing + '--> False:')
		self.print_tree(node.false_branch, spacing + "  ")

class Question:
	def __init__(self, column, value):
		self.column = column
		self.value = value

	def match(self, example):
		val = example[self.column]
		if self.is_numeric(val):
			return val >= self.value
		else:
			return val == self.value

	def __repr__(self):
		condition = "=="
		if self.is_numeric(self.value):
			condition = ">="
		return "Is %s %s %s?" % (
			header[self.column], condition, str(self.value))

	def is_numeric(self, value):
		return isinstance(value, int) or isinstance(value, float)

class Leaf(DesisionTree):
	def __init__(self, rows):
		self.predictions = self.class_counts(rows)

class Decision_Node:
	def __init__(self, question, true_branch, false_branch):
		self.question = question
		self.true_branch = true_branch
		self.false_branch = false_branch

if __name__ == "__main__":
	DesisionTree(train_data)
	NaiveBayes(train_data, test_data)