import numpy as np
import cv2

# 视频的读入
cap = cv2.VideoCapture(0)

# 构建角点检测所需参数
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)
# Parameters for lucas kanade optical flow
# maxLevel 为使用的图像金字塔层数
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0, 255, (100, 3))

# 拿到第一帧图像并灰度化作为前一帧图片
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
# 创建一个mask, 用于进行横线的绘制
mask = np.zeros_like(old_frame)

while True:
    # 读取图片灰度化作为后一张图片的输入
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 进行光流检测需要输入前一帧和当前图像及前一帧检测到的角点
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # 读取运动了的角点st == 1表示检测到的运动物体，即v和u表示为0
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    # 绘制轨迹
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (int(a),int(b)), (int(c),int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
    # 将两个图片进行结合，并进行图片展示
    img = cv2.add(frame, mask)
    cv2.imshow('frame', img)

    k = cv2.waitKey(30)& 0xff
    if k == ord('q'):
        break
    # 更新前一帧图片和角点的位置
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cv2.destroyAllWindows()
cap.release()
