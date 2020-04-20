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