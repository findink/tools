import sys
import math

def encode(filePath):
    origin = open(filePath,'r')
    origin_str = ''
    for line in origin: # 将文件合成一个字符串.
        origin_str += line
    site_dict = getSiteDict(origin_str)
    low,high = 0,1
    f = open(sys.path[0]+"/encoded.txt",'w')
    for c in origin_str:
        low_ = low +  (high-low)*site_dict[c][0]
        high_ = low + (high-low)*site_dict[c][1]
        low,high = low_,high_
        if high - low < 1e-3:
            low *= 100
            high *= 100
            store_num = math.floor(low)
            if store_num != 0:
                f.write(str(store_num))
                low -= store_num
                high -= store_num
    f.write(str(low).replace('.',''))
    print(low,high)

    

    
    
def getSiteDict(origin_str):
    char_dict = {}
    for c in origin_str: # 统计各个字符的出现次数
        if c in char_dict.keys():
            char_dict[c] += 1
        else:
            char_dict.update({c:1})
    char_ratio_dict = {}
    site_dict = {}
    origin_str_len = len(origin_str)
    low = 0
    for (k,v) in char_dict.items():
        ratio = v/origin_str_len
        char_ratio_dict.update({k:ratio})
        site_dict.update({k:[low,low + ratio]})
        low += ratio
    return site_dict



def decode():
    pass

encode(sys.path[0]+"/origin.txt")