# -*- coding: utf-8 -*-
from PIL.Image import new
import cv2


def reizevideo(video, resize_width, resize_height):
     cap = cv2.VideoCapture(video)#读取视频文件
     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
 
     out = cv2.VideoWriter('newrize300_300.mp4',fourcc, 20.0, (resize_width,resize_height),True)   
     while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:#如果读取失败，直接break
            
            break
            
        [height,width,pixels]= frame.shape #获取图片大小
        print(height,width,pixels)
        new_img = cv2.resize(frame, (int(resize_width), int(resize_height)), interpolation=cv2.INTER_CUBIC)#缩小图像
        #cv2.imshow("new_video", new_img)# 显示图像
        out.write(new_img)
     
     print("finished!")
     cap.release()# 释放摄像头或视频文件
     out.release()
     cv2.destroyAllWindows()#销毁所有窗口


if __name__=="__main__":
    print("开始修改视频尺寸")
    reizevideo("data/images/out.mp4",300,300)
