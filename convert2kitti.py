# Yolo txt标签格式转换至Kitti txt标签格式
import os
import cv2
import time


kittiPath = 'kittilabel'  # 新生成的kitti数据想存放的文件夹路径，根据需要修改
if os.path.exists(kittiPath) == False:
    os.makedirs(kittiPath)

# class names
labels = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]

a = []
for i in range(len(labels)):
    a.append(str(i))
b = zip(a,labels)
dict_label = dict(b)
#print(dict_label)

# 将txt中坐标还原到原始照片的坐标
def restore_coordinate(yolo_bbox, image_w, image_h):
    #print("yolo_bbox:",yolo_bbox)
    box_w = float(yolo_bbox[3]) * image_w
    box_h = float(yolo_bbox[4]) * image_h
    x_mid = float(yolo_bbox[1]) * image_w + 1
    y_mid = float(yolo_bbox[2]) * image_h + 1
    xmin = int(x_mid - box_w / 2)
    xmax = int(x_mid + box_w / 2)
    #ymin = int(y_mid - box_h / 2) + 5  # 增加了一个偏移的量5；
    #ymax = int(y_mid + box_h / 2) + 5
    ymin = int(y_mid - box_h / 2)   # 增加了一个偏移的量5；
    ymax = int(y_mid + box_h / 2) 
    return [xmin, ymin, xmax, ymax]



def restore_noneed_img(labels_folder,width,height):
    labels = os.listdir(labels_folder)
    for label in labels:
        name = label.split('.')[0]
        #print('name',name)
        with open(os.path.join(labels_folder, label), 'r') as f:
            #print("process label:",os.path.join(labels_folder,label))
            w = width
            h = height
            info = f.readline()
            #print("info:",info)
            lines = ""
            while info:
                label = list(info.split(' '))
                #print("label:",label)
                labelname = dict_label[label[0]]
                #print("labelname:",labelname)
                ori_box = restore_coordinate(label, w, h)
                new_info = labelname + ' ' + '0.00' + ' ' + '0' + ' ' + '0.00' + ' ' \
                           + str(ori_box[0]) + ' ' + str(ori_box[1]) + ' ' + str(ori_box[2]) + ' ' + str(ori_box[3]) \
                           + ' ' + '0.00' + ' ' + '0.00' + ' ' + '0.00' + ' ' + '0.00' + ' ' + '0.00' \
                           + ' ' + '0.00' + ' ' + '0.00' + '\n'
                lines += new_info
                info = f.readline()
            with open(os.path.join(kittiPath, name + '.txt'), 'w') as fn:
                fn.writelines(lines)
            fn.close()
            # 将转换的坐标值绘制到原始图片上，并显示查看
            # cv2.rectangle(img, (ori_box[0], ori_box[1]), (ori_box[2], ori_box[3]), (0, 255, 255), 2)
            # cv2.imshow('Transfer_label', img)
            # if cv2.waitKey(100) & 0XFF == ord('q'):
            #      break
        f.close()


def splittingData(labels_folder,image_width,image_height,savepath,savefile):
    absfilepath = os.path.join(savepath,savefile)
    with open(absfilepath,"w") as file:
        print("打开新建的label文件{}".format(absfilepath))

        #listdir 顺序是乱序排列的，所以要文件名排序
        labels = os.listdir(labels_folder)
        labels.sort(key=lambda x:int(x.split(".")[0].split("_")[1]))
        frame_num = 0
        for label in labels:
            with open(os.path.join(labels_folder, label), 'r') as f:
                #print("process label:",os.path.join(labels_folder,label))
                w = image_width
                h = image_height
                info = f.readline()
                #print("info:",info)
                lines = ''
                while info:
                    label = list(info.split(' '))
                    print("label:",label)
                    labelname = dict_label[label[0]]
                    #print("labelname:",labelname)
                    ori_box = restore_coordinate(label, w, h)
                    new_info = str(frame_num)+","+"-1," + str(ori_box[0]) + ',' + str(ori_box[1]) + ',' + str(ori_box[2]-ori_box[0]) + ',' + str(ori_box[3]-ori_box[1]) \
                            + ','+str(label[5])
                    lines += new_info     
                    info = f.readline()    
                file.writelines(lines)      
            f.close()
            frame_num+=1
    file.close()



# 获取照片的labels文件和images文件，并生成新的标签文件
def restore_results(images_folder, labels_folder):
    labels = os.listdir(labels_folder)
    for label in labels:
        name = label.split('.')[0]
        #print('name',name)
        with open(os.path.join(labels_folder, label), 'r') as f:
            #print("process label:",os.path.join(labels_folder,label))
            img = cv2.imread(os.path.join(images_folder, name + '.jpg'))
            w = img.shape[1]
            h = img.shape[0]
            
            info = f.readline()
            #print("info:",info)
            lines = ""
            while info:
                label = list(info.split(' '))
                #print("label:",label)
                labelname = dict_label[label[0]]
                #print("labelname:",labelname)
                ori_box = restore_coordinate(label, w, h)
                new_info = labelname + ' ' + '0.00' + ' ' + '0' + ' ' + '0.00' + ' ' \
                           + str(ori_box[0]) + ' ' + str(ori_box[1]) + ' ' + str(ori_box[2]) + ' ' + str(ori_box[3]) \
                           + ' ' + '0.00' + ' ' + '0.00' + ' ' + '0.00' + ' ' + '0.00' + ' ' + '0.00' \
                           + ' ' + '0.00' + ' ' + '0.00' + '\n'
                lines += new_info
                info = f.readline()
            with open(os.path.join(kittiPath, name + '.txt'), 'w') as fn:
                fn.writelines(lines)
            fn.close()
            # 将转换的坐标值绘制到原始图片上，并显示查看
            # cv2.rectangle(img, (ori_box[0], ori_box[1]), (ori_box[2], ori_box[3]), (0, 255, 255), 2)
            # cv2.imshow('Transfer_label', img)
            # if cv2.waitKey(100) & 0XFF == ord('q'):
            #      break
        f.close()
    # cv2.destoryAllWindows()


if __name__ == '__main__':
    s = time.time()
    imagePath = 'data/images'  # 原本的yolo数据格式的images所在的文件夹，根据自己的修改
    labelPath = 'runs/detect/exp/labels'  # 原本的yolo数据格式的labels所在的文件夹，根据自己的修改
    print('----数据转换开始---')

    command = input("选则传统的生成分开的KITTI 选1，选择生成抛洒物检测的数据选2\n")
    if command == "1":
        try:
            # 默认还是带着图反推，其实没必要，只是延续之前的操作
            restore_results(imagePath, labelPath)
        except:
            print("无图输入，直接使用默认的图片大小回复kitti format data")
            restore_noneed_img(labelPath, 960,720)
    elif command == "2":
        print("选择生成抛洒物的标签")
        splittingData(labelPath,960,720,"kittilabel","shiyan.txt")


    print('---耗时：{:.3f}ms'.format(time.time() - s))
    print('---数据转换成功---')
