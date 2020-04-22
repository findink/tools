import sys
import math
from collections import Counter

class arithmeticCoding():
    char_ratio_dict = {}
    site_dict = {}
    origin_str = ''
    
    def __init__(self):
        pass
    def encode(self,filePath):
        origin = open(filePath,'r')
        for line in origin: # 将文件合成一个字符串.
            self.origin_str += line
        self.site_dict = self.getSiteDict()
        low,high = 0,1
        f = open(sys.path[0]+"/encoded.txt",'w')
        for c in self.origin_str:
            low_ = low +  (high-low)*self.site_dict[c][0]
            high_ = low + (high-low)*self.site_dict[c][1]
            low,high = low_,high_
            if high - low < 1e-5: # 移动小数点, 将整数部分存入文件
                low *= 1e2
                high *= 1e2
                store_num = math.floor(low)
                if store_num < 10:
                    f.write('0')
                if store_num == 0:
                    f.write('0')
                if store_num != 0:
                    f.write(str(store_num))
                    low -= store_num
                    high -= store_num
        f.write(str(low).replace('.',''))



    def getSiteDict(self):
        char_dict = Counter(self.origin_str)
        origin_str_len = len(self.origin_str)
        low = 0
        for (k,v) in char_dict.items():
            ratio = v/origin_str_len
            self.site_dict.update({k:[low,low + ratio]})
            low += ratio
        return self.site_dict


    def getCharBySite(self,site):
        for k,v in self.site_dict.items():
            if  v[0] < site <v[1]:
                return k

   
    def leftandCut(self,n):
        if len(str(n)) < 16:
            flag = False
        else:
            flag = True
        m = n
        tail = str(n)[10:15] # 保存尾部
        n *= 100
        s = str(n)
        if m >= 1 and n >=100: # 整数消去大于100的部分
            if float(str(n)[2:10]) < 10 and m >10:
                s = str(n)[3:10] + tail
            else:
                s = str(n)[2:10] + tail
        elif m < 1 and n >10:  # 只少一位
            s = str(n)[0:9] + tail
        elif m<1 and n < 10: # 少两位
            s = str(n)[0:8] + tail
        if flag:
            s += '2'
        t = float(s)
        return t

    def decode(self,filePath):
        f = open(filePath,'r')
        r = ''
        decoded_str = '0.'
        for line in f:
            decoded_str += line
        print(decoded_str)
        str_len = len(decoded_str)
        i,j,max_len = 0,15,100
        # k = 1.0
        num = float(decoded_str[i:j]+'1')
        count = 0
        low,high = 0,1
        while len(str(num))>5 and count < max_len:
            count += 1
            num_ = float(str(num)[0:-1])
            flag = 0
            for k,v in self.site_dict.items():
                low_ = low +  (high-low)*v[0]
                high_ = low + (high-low)*v[1]
                if low_ <= math.modf(num_)[0] <= high_:
                    flag = 1
                    r += k
                    low,high = low_,high_
                    break
            if flag ==0:
                print('decode failed! get:',r)
                return
            if high - low < 1e-3:
                num = self.leftandCut(num)
                low *= 1e2
                high *= 1e2
                store_num = math.floor(low)
                low -= store_num
                high -= store_num 
                d = 16 - len(str(num))
                i = j
                j = min(j+ d ,str_len)
                if i != str_len:
                    num_str = str(num)[0:-1] + decoded_str[i:j] + '1'
                    # print(num_str)
                    num = float(num_str) 
        print(r)   
        f1 = open(sys.path[0]+'/decoded.txt','w')
        f1.write(r)   
        f1.close()    

            



if __name__ == "__main__":
    coding = arithmeticCoding()    
    coding.encode(sys.path[0]+"/origin.txt")
    # print(arithmeticCoding.site_dict)
    coding.decode(sys.path[0]+"/encoded.txt")