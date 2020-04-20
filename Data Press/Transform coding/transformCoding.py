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

            



def getDCT(N):
    A = np.zeros((N,N))
    temp_list = z_scan(N)
    for i in range(N):
        if i == 0:
                ak = np.sqrt(1/N)
        else:
                ak = np.sqrt(2/N)
        for j in range(N):
            if [i,j] in temp_list[:8]:
                b = ((2*j + 1) * i * np.pi)/(2*N)
                A[i][j] = ak * np.cos(b)
    return A




def trans(N,img):
    A = getDCT(N)
    A = np.matrix(A)
    wight,height = img.shape
    img2 = np.matrix(np.zeros(img.shape))
    for i in range(int(wight/N)):
        for j in range(int(height/N)):
            x = img[i*N:i*N+N,j*N:j*N+N] 
            img2[i*N:i*N+N,j*N:j*N+N] = A * x * A.T
            

    return img2

def recover(N,img2):
    A = getDCT(N)
    A = np.matrix(A)
    wight,height = img2.shape
    img3 = np.matrix(np.zeros(img2.shape))
    for i in range(int(wight/N)):
        for j in range(int(height/N)):
            x = img2[i*N:i*N+N,j*N:j*N+N] 
            img3[i*N:i*N+N,j*N:j*N+N] = A.T * x * A
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

    img0 = img
    img = img -128
    print(np.max(img))
    N = 8
    p2 = trans(N,img)
    p3 = recover(N,p2) 
    p3 = p3 + 128
    cv2.imwrite('./img_test2.bmp', p2)
    cv2.imwrite('./img_test3.bmp', p3)

    print(getPSNR(img0,p3))