import cv2
import numpy as np 



def z_scan(N):
    temp_list = []
    i,j =0,0
    temp_list.append([i,j])
    j += 1
    temp_list.append([i,j])
    while i+j < 2*(N -1):
        while j != 0 and i < N -1:
            j -= 1
            i += 1
            temp_list.append([i,j])
        if i + j<N-1:
            i += 1
            temp_list.append([i,j])
        else:
            j += 1
            temp_list.append([i,j])
        while i != 0 and j < N -1:
            i -= 1
            j += 1
            temp_list.append([i,j])
        if i+j <N:
            j += 1
            temp_list.append([i,j])
        else:
            i += 1
            if i< N:
                temp_list.append([i,j])
    return temp_list

def trans(N,img):
    wight,height = img.shape
    img2 = np.matrix(np.zeros(img.shape))
    img2.astype(np.float)
    for i in range(int(wight/N)):
        for j in range(int(height/N)):
            x = img[i*N:i*N+N,j*N:j*N+N] 
            img2[i*N:i*N+N,j*N:j*N+N] = cv2.dct(x)
    return img2

def recover(N,img2):
    wight,height = img2.shape
    img3 = np.matrix(np.zeros(img2.shape))
    img3.astype(np.float)
    for i in range(int(wight/N)):
        for j in range(int(height/N)):
            x = img2[i*N:i*N+N,j*N:j*N+N] 
            temp_list = z_scan(N)[0:8]
            for k in range(N):
                for l in range(N):
                    if [k,l] not in temp_list: 
                        x[k,l] = 0
            img3[i*N:i*N+N,j*N:j*N+N] = cv2.idct(x)
    return img3

def getPSNR(img1,img2):
    diff = img1 - img2
    mse = np.mean(np.square(diff))
    psnr = 10 * np.log10(255 * 255 / mse)
    return psnr

if __name__ == "__main__":
    img = np.fromfile('Data Press\Transform coding\lena.raw',dtype=np.uint8)
    img = img.reshape(512,512)
    img = np.matrix(img)
    img = img.astype(np.float)
    print(np.mean(img))
    N = 8
    p2 = trans(N,img)
    p3 = recover(N,p2) 
    cv2.imwrite('./img_test2.bmp', p2)
    cv2.imwrite('./img_test3.bmp', p3)
    print(getPSNR(img,p3))