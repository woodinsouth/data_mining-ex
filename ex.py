
from fp import apriori
from classify import NaiveBayes,DesisionTree
from cluster import kmeans
from optparse import OptionParser

# the classifcation data
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

if __name__ == "__main__":

	optparser = OptionParser()
	optparser.add_option('--mins', dest='min_support', help='minium support value', default=0.6, type='float')
	optparser.add_option('--k', dest='k', help='kmeans k center point', default=3, type=int)

	(options, args) = optparser.parse_args()
	# find frequent itemset in the dataset in textbook
	min_support = options.min_support
	apriori("apriori_d.txt", min_support)

	# classify the test data by the classfier trained by the train data in the textbook, which is write in the code module
	DesisionTree(train_data)
	NaiveBayes(train_data, test_data)

	# cluster the dataset in textbook
	k = options.k
	textbook = kmeans("kmeans_t.txt", k)