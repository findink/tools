import cv2
import numpy as np 


# z型扫描顺序列表, 取前k个
def z_scan():
    temp_list = []
    i,j =0,0
    temp_list.append([i,j])
    j += 1
    temp_list.append([i,j])
    while i+j < 2*(8 -1):
        while j != 0 and i < 8 -1:
            j -= 1
            i += 1
            temp_list.append([i,j])
        if i + j<8-1:
            i += 1
            temp_list.append([i,j])
        else:
            j += 1
            temp_list.append([i,j])
        while i != 0 and j < 8 -1:
            i -= 1
            j += 1
            temp_list.append([i,j])
        if i+j <8:
            j += 1
            temp_list.append([i,j])
        else:
            i += 1
            if i< 8:
                temp_list.append([i,j])
    return temp_list

            
# 获得DCT变换矩阵
def getDCT():
    A = np.zeros((8,8))
    for i in range(8):
        if i == 0:
                ak = np.sqrt(1/8)
        else:
                ak = np.sqrt(2/8)
        for j in range(8):
                b = ((2*j + 1) * i * np.pi)/(2*8)
                A[i][j] = ak * np.cos(b)
    return A

# 对每一个block进行dct
def DCT(img):
    A = getDCT()
    A = np.matrix(A)
    wight,height = img.shape
    img_dct = np.matrix(np.zeros(img.shape))
    for i in range(int(wight/8)):
        for j in range(int(height/8)):
            x = img[i*8:i*8+8,j*8:j*8+8] 
            img_dct[i*8:i*8+8,j*8:j*8+8] = A * x * A.T
    return img_dct.astype(np.int16)

#  对每一个block进行还原
def IDCT(img_dct):
    A = getDCT()
    A = np.matrix(A)
    wight,height = img_dct.shape
    img_idct = np.matrix(np.zeros(img_dct.shape))
    for i in range(int(wight/8)):
        for j in range(int(height/8)):
            x = img_dct[i*8:i*8+8,j*8:j*8+8]
            temp_list = z_scan()[0:coff_num]
            for k in range(8):
                for l in range(8):
                    if [k,l] not in temp_list: 
                        x[k,l] = 0
            img_idct[i*8:i*8+8,j*8:j*8+8] = A.T * x * A
    return img_idct.astype(np.int16)

# 计算PSNR
def getPSNR(img1,img_dct):
    diff = img1 - img_dct
    mse = np.mean(np.square(diff))
    psnr = 10 * np.log10(255 * 255 / mse)
    return psnr


# 量化与反量化
def Quantification(img,forward):
    table =  [[16,11,10,16,24,40,51,61,],
        [12,12,14,19,26,58,60,55,],
        [14,13,16,24,40,57,69,56,],
        [14,17,22,29,51,87,80,62,],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99] ]
    table = np.matrix(table)
    table = table * QTF_time
    wight,height = img.shape
    img_QTF = np.matrix(np.zeros(img.shape))
    if(forward == True):
        for i in range(int(wight/8)):
            for j in range(int(height/8)):
                x = img[i*8:i*8+8,j*8:j*8+8]
                img_QTF[i*8:i*8+8,j*8:j*8+8] = x / table 
    else:
        for i in range(int(wight/8)):
            for j in range(int(height/8)):
                x = img[i*8:i*8+8,j*8:j*8+8]
                img_QTF[i*8:i*8+8,j*8:j*8+8] = np.multiply( x ,table)
    return img_QTF.astype(np.int16)


if __name__ == "__main__":
    img = np.fromfile('lena.raw',dtype=np.uint8)

    img = img.reshape(512,512)  
    cv2.imwrite('img_origin.bmp', img)
    img = np.matrix(img)
    img = img.astype(np.int16)

    coff_num = 64 # 还原时,取前coff_num个系数
    QTF_time = 4 # 量化时k的值

    img0 = img # 保存原始图像
    img = img -128  # 幅值移动
    img_dct = DCT(img) # dct
    
    img_QTF = Quantification(img_dct,True) # 量化
    img_iQTF = Quantification(img_QTF,False)# 反量化
    img_idct = IDCT(img_iQTF)   # 还原
    img_idct = img_idct + 128

    cv2.imwrite('img_dct.bmp', img_dct)
    cv2.imwrite('img_idct.bmp', img_idct)
    
    print('coefficient number:',coff_num)
    print('quantization k:',QTF_time)                                                                      
    print('PSNR:',getPSNR(img0,img_idct))