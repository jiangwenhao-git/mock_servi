def tag2dict(filepath):
	with open(filepath,'r',encoding='utf-8') as f:
		dic = []
		for line in f.readlines():
			line = line.strip('\n')
			b = line.split(' ')
			dic.append(b)
	dic = dict(dic)
	return dic

ReturnCode = tag2dict('UsLmtChg.tag')['s:ReturnCode']
Returndicts = tag2dict('UsLmtChg.tag')
for returndict in Returndicts.items():
	print(returndict)
print(tag2dict('UsLmtChg.tag').values())