# -*- coding:utf-8 -*-

import numpy as np
import cv2
import time,datetime
import threading

# 每次检测到运动 抓取视频长度
RECORD_SECENDS = 10
# 每秒帧数 流畅度
FPS = 2
# 保存视频文件类型
FOURCC = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

camera = cv2.VideoCapture(0)
# 选取摄像头 0为默认摄像哦图
if camera is None:
    print('Please check camera.')
    exit()

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
pre_frame = None  # 总是取前一帧做为背景（不用考虑环境影响）
out_file =None
# 是否正在录制
is_motion = False
is_start = False
left_secends = RECORD_SECENDS

def add_frame(frame):
    # 反转贞
    # frame = cv2.flip(cur_frame, 1)
    text = "Hello World!"
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    out_file.write(frame)
    print('add frame')

while True:
    start = time.time()
    # 从摄像头读取一帧
    res, cur_frame = camera.read()
    frame = cur_frame
    if res != True:
        print('未获取到贞 check camera.')
        # break
        continue

    gray_img = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (500, 500))
    gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)

    if pre_frame is None:
        pre_frame = gray_img
    else:
        img_delta = cv2.absdiff(pre_frame, gray_img)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print('is_motion init False.')
        is_motion = False
        for c in contours:
            if cv2.contourArea(c) < 1000:  # 设置敏感度
                print('is_motion set False.')
                is_motion = False
                continue
            else:
                # print(cv2.contourArea(c))
                print("前一帧和当前帧不一样了, 有什么东西在动! 开始记录")
                print('is_motion set True.')
                is_motion = True
                break
        pre_frame = gray_img
    print('is_motion '+str(is_motion)+' is_start ' + str(is_start))
    # 如果检测到运动 录像时间延长
    if not is_motion and not is_start:
        left_secends = 0
        pass
    if is_motion and not is_start:
        is_start = True
        left_secends = RECORD_SECENDS
        # 创建out文件
        file_name = 'test_video/video_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.avi'
        out_file = cv2.VideoWriter(file_name,cv2.VideoWriter_fourcc('M','J','P','G'), FPS, (frame_width,frame_height))
        print('create out file ' + file_name)
        add_frame(frame)
    if not is_motion and is_start:
        if left_secends > 0.1:
            add_frame(frame)
        else:
            print('is_start set False release out_file.')
            is_start=False
            out_file.release()
            left_secends = 0
    if is_motion and is_start:
        # 延长录制时间
        print('delay time')
        left_secends = RECORD_SECENDS
        add_frame(frame)
    end = time.time()
    seconds = end - start
    # 每秒获取几张
    if seconds < 1.0 / FPS:
        time.sleep(1.0 / FPS - seconds)
    left_secends = left_secends - 1.0 / FPS
    print('left_secends: '+ str(left_secends) +'s.')

camera.release()
cv2.destroyAllWindows()
