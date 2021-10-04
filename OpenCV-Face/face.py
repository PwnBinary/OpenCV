import os   # 导入操作系统接口模块

import face_recognition   # 导入人脸库
import cv2   # 导入opencv的库

from message import *   # 导入发送消息模块

# 读取数据库中的人名和面部特征
# 1.准备工作
targetName = ['HeZhiYu']   # 目标人物名字
face_databases_dir = 'databases'   # 定义数据库的变量名
user_names = []   # 存储用户的姓名
user_faces_encodings = []   # 存储面部特征

# 2.正式工作
# 2.1 得到face_database_dir 文件夹下所有的文件名
files = os.listdir('databases')   # 读取文件名

# 2.2 循环读取文件名并做进一步的处理
for image_shot_name in files:
    # 2.2.1 截取文件名.前半部分作为用户名存入user_names列表中
    user_name, _ = os.path.splitext(image_shot_name)   # 返回两个值，分别为.前面的和.后面的
    user_names.append(user_name)   # 将对象放入用户名列表列表

    # 2.2.2 读取图片文件中的面部特征信息存入user_faces_encodings列表中
    image_file_name = os.path.join(face_databases_dir, image_shot_name)   # 将路径拼接在一起

    image_file = face_recognition.load_image_file(image_file_name)   # 加载图片
    face_encodings = face_recognition.face_encodings(image_file)[0]   # 读取图片特征信息，返回一个数组，有可能返回多个脸部特征信息,这里用数组下标访问

    user_faces_encodings.append(face_encodings)   # 将面部特征放到列表


# 1.打开摄像头，读取摄像头的画面
# 定位到画面中人的脸部，并用绿色的框把人脸框住

# 2.读取到数据库中的人名和脸部特征

# 3.用拍摄到的人脸部特征和数据库中的脸部特征做匹配
# 并在用户头像的绿框上方用用户的姓名做标识，未知用户统一使用Unkown

# 4.定位和锁定目标人物，改使用红色的框把目标人物框住


# 1.打开摄像头，获取摄像头对象
video_capture = cv2.VideoCapture(0)   # 捕获摄像头，默认索引从0开始

# 2.循环不停的获取拍摄到的画面，并做进一步的处理
while True:
    # 2.1 获取摄像头拍摄到的画面
    ret, frame = video_capture.read()   # 读取摄像头画面并返回参数，默认返回两个参数，第一个代表有没有返回画面，第二个代表画面本身

    # 2.2 从拍摄到的画面中提取出人脸部所在区域(可能会有多个)
    face_locations = face_recognition.face_locations(frame)   # 传入画面参数，返回人脸部所在区域,返回一个列表数据,如果有多个，返回多个列表

    ## 2.21 从所有人头像所在区域提取脸部特征
    face_encodings = face_recognition.face_encodings(frame, face_locations)   # 第一个参数为画面，第二个参数为所在区域，该函数返回所在区域的面部特征
    ## 2.22 定义用于存储拍摄到的用户的姓名的列表,如果特征匹配不上数据库中的特征，则报错
    names = []
    ## 遍历拍摄拍摄到的面部特征和数据库中的面部特征做匹配
    for face_encoding in face_encodings:
        # compare_faces(['面部特征1', '面部特征2'], 未知的面部特征)
        # 假如和面部特征1匹配，则返回[True, False, False]
        matchs = face_recognition.compare_faces(user_faces_encodings,face_encoding)   # 第一个参数是数据库列表，第二个参数是单个的面部特征

        name = "Don't know you"   # 定义默认为unknown
        for index, is_match in enumerate(matchs):   # 拉到matchs列表的索引
            # [False, True, False]
            # 0, False
            # 1, True
            # 0, False
            if is_match:
                name = user_names[index]   # 当为True的时候将索引放到user_names中,并将索引对应的值赋值给name变量
                break   # 如果匹配到了则退出循环
        names.append(name)   # 将匹配到的name放到names列表中

    # 2.3 循环遍历人脸部所在区域并画框,在框上标识人的姓名
    # zip(['第一个人的位置'，'第二个人的位置'], ['第一个人的姓名'，'第二个人的姓名'])
    # for
    # 1: ‘第一个人的位置‘，‘第一个人的姓名’
    # 2: ...

    for (top, right, bottom, left), name in zip(face_locations, names):   # 将face_locations拆包, (前面是位置，后面是姓名)
        color = (0, 0, 255)   # 定义默认颜色
        if name in targetName:
            # BGR
            color = (0, 255, 0)
            send()   # 发送信号

        # 在人像所在区域画框
        # 参数1为在哪个图像画框
        # 参数2参数3为框的坐标
        # 参数4为框的颜色(这里用RGB，但在opencv中颜色的倒过来的)
        # 参数5为线条的宽度
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)   # 通过rectangle参数画框
        font = cv2.FONT_HERSHEY_DUPLEX   # 定义字体
        # putText 写字
        # 参数1: 在哪张图片写字
        # 参数2: 要写的内容
        # 参数3: 要写字的坐标 (一个点就行)
        # 参数4: 字体
        # 参数5: 字的大小
        # 参数6: 字的颜色
        # 参数7: 字的宽度
        cv2.putText(frame, name, (left, top-10), font, 0.5, color, 1)

    cv2.namedWindow("Video", 0)   # 创建窗口
    cv2.resizeWindow("Video", 1536, 864)   # 定义窗口的大小
    cv2.imshow("Video", frame)   # 通过opencv把画面展示出来,第一个参数为窗口的名字，第二个为展示的图片

    # 设定按q退出while循环,退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):   # 1代表截取1帧的图像，ord为q的ASCII码,waitKey返回值的范围为0~255
        # 退出while循环
        break

# 3.退出程序的时候，释放摄像头资源
video_capture.release()   # 释放摄像头资源
cv2.destroyAllWindows()   # 关闭所有窗口
