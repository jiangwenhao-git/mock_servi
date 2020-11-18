import xmltodict
import collections
data = {"s:ReturnCode":"88888888"}

# a = data.split('-')
#
# file_dic = dict()
# n = len(a)
# def fun(n,i=0,dict1={}):
#     if i == n-1:
#         dict1[a[i]] = a[i+1:]
#     if i < n -1:
#         dict1[a[i]] = fun(n,i+1,dict1={})
#     return dict1
#
#
# print(fun(n-1).values())

def list_dict(d,n_tab = -1):
    if isinstance(d,list):
        for i in d:
            list_dict(i,n_tab)

def _finditem(obj,key,value):
    if key in obj:
        obj[key] = value
        return obj
    for k,v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v,key,value)
            if item is not None:
                return item
    # return xmltodict.unparse(obj)



def dispose_dict(input_parameter,fixed_parameter):
    for input_key, input_value in input_parameter.items():
        for fixed_key, fixed_value in fixed_parameter.items():
            if input_key == fixed_key:
                if isinstance(fixed_parameter[fixed_key],str):
                    fixed_parameter[fixed_key] = input_value
                    break
                elif isinstance(fixed_parameter[fixed_key],list):
                    if len(fixed_parameter[fixed_key]) == 0:
                        fixed_parameter[fixed_key].append(input_value)
                        break
            elif isinstance(fixed_value, dict):
                if len(fixed_value) != 0:
                    dispose_dict(input_parameter,fixed_value)
            elif isinstance(fixed_value, list):
                if len(fixed_value) != 0:
                    if isinstance(fixed_value[0], dict):
                        for kv1 in fixed_value:
                            dispose_dict(input_parameter, kv1)

    return fixed_parameter




#++++++++++++++++++++++++++++++++++++++++++
filepath = './UsLmtChg.xml'
# list_dir = data.split(' ')[0]
# list_value = data.split(' ')[1]
def mock_handler(mockfile):
    file_dic = xmltodict.parse(mockfile)
    print("dispose_dict   :",dispose_dict(data, file_dic))
    print(file_dic)
    dictobj = dispose_dict(data,file_dic)
    dictobjtoxml = xmltodict.unparse(dictobj)
    f = open(filepath,'w')
    f.write(dictobjtoxml)
    f.close()
    # dictobj = _finditem(file_dic,list_dir,list_value)
    # dictobjtoxml = xmltodict.unparse(dictobj)
    # f = open(filepath,'w')
    # f.write(dictobjtoxml)
    # f.close()



#参考上次写的对xml文件的定位写入修改
if __name__ == '__main__':
    file = open(filepath)
    mock_file = file.read()
    mock_handler(mock_file)
    file.close()

#++++++++++++++++++++++++++++++++++++++++++++

# i = 0
# print(len(data_path))
# for data_num in data_path:
#     if i < len(data_path):
#         file_dic.update({data_path[i]: ''})
#         i = i+1
#
# print(list_tmp[1])
# print(list_tmp[0])
# print(data_path)
# print(file_dic)