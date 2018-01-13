from random import randint

class kmeans(object):
	def __init__(self, file, k):
		print(str(k) + " cluster result")
		self.k = k
		self.file = file
		self.data = self.load_data(self.file)
		self.k_means(self.data, self.k)
		print("----------------------------------------------------")

	# read txt file into 2d float array(list)
	def load_data(self, file):
		with open(file,'r') as f:
			data = []
			for point in f:
				point_xy = []
				for i in point.split():
					point_xy.append(float(i))
				data.append(point_xy)
		return data

	def k_means(self, data, k):
		# the x-y coodinate values of center points, whose size is k*2 
		center = []
		# the cluster index of all points, whose size is len(data)
		cluster = []
		center_count = k
		num = len(data)

		# initializing random center points
		while len(center)<k:
			i = randint(0,num-1)
			if center.count(i)==0:
				center.append(data[i])

		# clustering and recomputing center points until stable
		while True:

			# clustering by center points
			for point in data:
				min_distance = float("inf")
				center_index = 0
				for c in center:
					distance = self.cal_distance(point,c)
					if  distance < min_distance:
						min_distance = distance
						cluster_index = center_index
					center_index += 1
				cluster.append(cluster_index)

			new_center = []
			
			# recompute center points based on the clustering result
			for cluster_index in range(k):
				sum = [0.0, 0.0]
				cluster_size = 0
				for point in range(num):
					if cluster[point] == cluster_index:
						cluster_size += 1
						sum[0] += data[point][0]
						sum[1] += data[point][1]
				if cluster_size==0:
					continue
				new_center.append([sum[0]/cluster_size, sum[1]/cluster_size])

			# print results and exit from the while loop when stable
			if new_center == center:
				self.print_cluster(cluster, data, k)
				break

			center = new_center

	def cal_distance(self, point, center):
		return (point[0]-center[0])**2+(point[1]-center[1])**2

	def print_cluster(self, cluster, data, k):
		for cluster_index in range(k):
			print("cluster " + str(cluster_index+1))
			for point in range(len(data)):
				if cluster[point] == cluster_index:
					print("A" + str(point+1))

if __name__ == "__main__":
	k = 3
	file = "kmeans_t.txt"
	textbook = kmeans(file, k)