with open('nonces.txt') as orig_values:
  nonces = [line.rstrip('\n') for line in orig_values]

count = 0
while count < len(nonces):
    nonces[count] = int(nonces[count])
    count += 1

for x in nonces:
    int64 = x
    int32_1 = int64 & 0xFFFFFFFF
    int32_2 = (int64 & (0xFFFFFFFF << 32) ) >> 32
    print("{0} | {1}".format(int32_1,int32_2))
    f = open("nonces_all.txt", "a")
    f.write(str(int32_1)+'\n')
    f.close()
    f2 = open("nonces_all.txt", "a")
    f2.write(str(int32_2)+'\n')
    f2.close()