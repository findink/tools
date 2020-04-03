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
            ratio = round(v/origin_str_len,4)
            self.site_dict.update({k:[low,low + ratio]})
            low += ratio
        return self.site_dict


    def getCharBySite(self,site):
        for k,v in self.site_dict.items():
            if  v[0] < site <v[1]:
                return k

    def leftandCut(self,n):
        tail = str(n)[10:15] # 保存尾部
        n *= 100
        s = str(n)
        if n >= 100: # 整数消去大于100的部分
            s = str(n)[2:10] + tail
        elif n >= 10:
            # w_len = 15 - len(str(n)) -2
            s = str(n)[0:8] + tail
        else:
            s = str(n)[0:8] + tail
        #  todo: 注意末尾的0会被去掉.
        t = float(s)
        return t

    def decode(self,filePath):
        f = open(filePath,'r')
        r = ''
        decoded_str = '0.'
        for line in f:
            decoded_str += line
        str_len = len(decoded_str)
        i,j = 0,15
        # k = 1.0
        num = float(decoded_str[i:j])
        count = 0
        # while count < 30:
        #     count += 1
        #     c = self.getCharBySite(num/k)
        #     r += c
        #     num -= self.site_dict[c][0] * k
        #     k *= self.site_dict[c][1] - self.site_dict[c][0]
        #     if k < 1e-5:
        #         num *= 1e2
        #         k *=   1e2
        #         d = 15 - len(str(num))
        #         if d > 0:
        #             i = j
        #             j = min(j+ d ,str_len)
        #             if j == str_len:
        #                 break
        #             num_str = str(num) + decoded_str[i:j]
        #             num = float(num_str) 
        # print(r)
        low,high = 0,1
        while count < 30:
            count += 1
            for k,v in self.site_dict.items():
                low_ = low +  (high-low)*v[0]
                high_ = low + (high-low)*v[1]
                if low_ < num < high_:
                    r += k
                    # print(k)
                    low,high = low_,high_
                if num - low < 1e-4:
                    num = self.leftandCut(num)
                    low = self.leftandCut(low)
                    high = self.leftandCut(high)
                    print(num)
                    d = 15 - len(str(num))
                    i = j
                    j = min(j+ d ,str_len)
                    if j == str_len:
                        break
                    num_str = str(num) + decoded_str[i:j]
                    # print(num_str)
                    num = float(num_str) 
        print(r)          

            



if __name__ == "__main__":
    coding = arithmeticCoding()    
    coding.encode(sys.path[0]+"/origin.txt")
    coding.decode(sys.path[0]+"/encoded.txt")