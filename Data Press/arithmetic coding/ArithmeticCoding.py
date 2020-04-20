import sys
import math
from collections import Counter

class arithmeticCoding():
    char_ratio_dict = {}
    site_dict = {}
    origin_str = ''
    encode_str = ''
    decode_str = ''
    
    def __init__(self):
        pass
    def encode(self,s):
        self.origin_str = s
        self.getSiteDict()
        low,high = 0,1
        for c in self.origin_str:
            low_ = low +  (high-low)*self.site_dict[c][0]
            high_ = low + (high-low)*self.site_dict[c][1]
            low,high = low_,high_
        self.encode_str =  str((low+high)/2)
        return self.encode_str

    def printDict(self):
        for k,v in self.site_dict.items():
            print(k,v)

    def getSiteDict(self):
        char_dict = Counter(self.origin_str)
        origin_str_len = len(self.origin_str)
        low = 0
        for (k,v) in char_dict.items():
            ratio = v/origin_str_len
            self.site_dict.update({k:[low,low + ratio]})
            low += ratio
    
    def decode(self,s):
        num = s
        low,high = 0,1
        while len(self.decode_str)< len(self.origin_str):
            num_ = float(str(num)[0:-1])
            for k,v in self.site_dict.items():
                low_ = low +  (high-low)*v[0]
                high_ = low + (high-low)*v[1]
                if low_ <= num_ <= high_:
                    self.decode_str += k
                    low,high = low_,high_
                    break
        return self.decode_str          

if __name__ == "__main__":
    coding = arithmeticCoding()  
    s = input('input a String:')  
    num = coding.encode(s)
    coding.printDict()
    print('Encode Number:',num)
    re = coding.decode(num)
    print('Decode Number:',re)