import sys
s=open(sys.argv[1]).read(); n=int(sys.argv[3]) if len(sys.argv)>3 else 45000
parts=[]; cur=''
for para in s.split('\n\n'):
    if len(cur)+len(para)>n and cur: parts.append(cur); cur=''
    cur+=para+'\n\n'
parts.append(cur)
for i,p in enumerate(parts): open(f"{sys.argv[2]}.{i}.txt",'w').write(p)
print(len(parts))
