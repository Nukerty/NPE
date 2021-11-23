import sys
import os

if not(len(sys.argv) == 4 and os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2])):
    raise Exception("Either 3 files are not considered or the path of files are messed up")

bigger_file = sys.argv[1]
smaller_file = sys.argv[2]
target_file = sys.argv[3]

with open(bigger_file, 'r') as big_file:
    data_bigger = big_file.read()
with open(smaller_file, 'r') as small_file:
    data_smaller = small_file.read()

data_bigger = [x for x in   data_bigger.split('\n') if len(x) > 0]
data_smaller= [x for x in   data_smaller.split('\n') if len(x) > 0]

bigger_data = set(data_bigger).union(set(data_smaller))

with open (target_file, 'w') as tf:
    for word in bigger_data:
        tf.write(f"{word}\n")
