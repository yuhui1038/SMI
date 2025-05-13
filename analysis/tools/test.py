import math


num_seqs = 177009652
x = 100000000 / num_seqs
y = 1 / num_seqs
time_s1j1 = 1 / num_seqs
a = time_s1j1 * math.log2(time_s1j1 / x / y)
print(math.log2(a))

x = 100 / num_seqs
y = 100 / num_seqs
time_s1j1 = 10 / num_seqs
b = time_s1j1 * math.log2(time_s1j1 / x / y)
print(math.log2(b))

print(math.log2(b) - math.log2(a))