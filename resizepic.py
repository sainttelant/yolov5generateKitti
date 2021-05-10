import cv2
import os

def img_resize(image):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    width_new = 960
    height_new = 544
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)),interpolation=cv2.INTER_AREA)
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new),interpolation=cv2.INTER_AREA)
    return img_new

if __name__=="__main__":

    imgspath = "data/images"
    allpics = os.listdir(imgspath)
    for imgs in allpics:
        abspathimg = os.path.join(imgspath,imgs)
        #print("abspathimg:",abspathimg)
        img = cv2.imread(abspathimg)
        img_new = img_resize(img)
        cv2.imwrite(abspathimg,img_new)
    print("finish resized all!!!!")
