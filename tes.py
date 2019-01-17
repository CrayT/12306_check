a=[3,1,4,6,0]
b=[]
for i in range(len(a)):
    if a[i] < 4:
        b.append(a[i])
print(b)

c={"1":"a"}
b=c
print(b)
a=b
print(a)