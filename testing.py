data = '11100111111111'

with open('test.txt' , 'w+b') as f:
    length = len(data)
    counter = 0
    while counter < length:
        f.write(bytes(int(data[counter:counter+2])))
        counter += 8
    for i in f.read():
        print(i)
        print(f.read())