import cv2
# 打开 Astra+摄像头
cap = cv2.VideoCapture(0)
i=0
while(1):
# frame 表示截取到一帧的图片
        ret,frame = cap.read()
        cv2.imshow('capture',frame)
        cv2.imwrite(r"/home/mowen/4_python_test/test_4_2_pictures/"+ str(i) + ".jpg",frame)
        i=i+1
#cv2.waitKey(1):waitKey()函数功能是不断刷新图像
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#释放对象和销毁窗口
cap.release()
cv2.destroyAllWindows()