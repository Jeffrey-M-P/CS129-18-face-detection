from mlp import MLP
import csv

def load_training(filename, brain):
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			data = [float(x) for x in row[:-1]]
			label = row[-1]

			target = [0]
			target[0] = (float(label))==1

			idealError = 0.3
			epoch = 10

			for i in range(epoch):
				currError = brain.overallNetError
				brain.feedForward(data)	

				output = brain.getOutputNeurons()				
				brain.backPropagate(target)

				if brain.overallNetError < currError:
					if brain.overallNetError < idealError:
						break

	return brain

def get_ann_label(data, brain):
	brain.feedForward(data)
	output = brain.getOutputNeurons()

	if output[0].val > 0:
		return 1
	else:
		return 0

def load_validation(filename, brain):
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		numCorrect = 0
		numTotal = 0

		for row in reader:
			data = [float(x) for x in row[:-1]]
			label = int(float(row[-1]))
			annLabel = get_ann_label(data, brain)

			if annLabel == label:
				numCorrect = numCorrect + 1
			numTotal = numTotal + 1

		print "Correct:", numCorrect
		print "Total: ", numTotal
		print "Accuracy: ", float(numCorrect)/float(numTotal)*100.0, "%"

# Create new MLP
def create_brain():
	topology = [32,64,16,8,1]
	brain = MLP(topology)
	brain = load_training('data/train.csv', brain)
	brain.saveNetwork()

	return brain
	
# Load existing topology from mlp.net
def get_brain():
	brain = MLP()
	return brain

if __name__ == '__main__': 
	# If you want to test on a new brain:
	brain = create_brain()

	# If you want to test on the existing brain:
	# brain = get_brain()

	# Run the tests
	load_validation('data/test.csv', brain)