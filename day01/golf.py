i=input()
print(sum(int(a)for a,b in zip(i,[*i[1:],i[0]])if a==b))
print(sum(int(a)for a,b in zip(i,i[len(i)//2:])if a==b)*2)
