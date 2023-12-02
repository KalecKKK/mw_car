import numpy as np
import cv2
import os
import shutil
import logging
import dlib
# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()
class Face_Register:
    def __init__(self):
        self.path_photos_from_camera = "test_4_8_data/data_faces/"
        self.font = cv2.FONT_ITALIC
        self.ss_cnt = 0                # 录入人脸时 图片计数器
        self.save_flag = 1             # 用于控制是否保存图像的 flag
    # 新建文件夹
    def pre_work_mkdir(self):
        if os.path.isdir(self.path_photos_from_camera):
            pass
        else:
            os.mkdir(self.path_photos_from_camera)
    # 新建文件夹--保存人脸图像
    def face_mkdir(self, name):
        path = os.path.join(self.path_photos_from_camera, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)
        self.ss_cnt = 0     # 将人脸计数器清零
        return path
    def process(self):
        cap = cv2.VideoCapture(0)
        # 新建文件夹
        self.pre_work_mkdir()
        name = input('Please enter your name:')
        # 新建文件夹--保存人脸图像
        current_face_dir = self.face_mkdir(name)
        while True:
            ret,frame = cap.read()
            kk = cv2.waitKey(1)
            faces = detector(frame, 0)     
            # 检测到人脸
            if len(faces) != 0:
                for k, d in enumerate(faces):
                    height = (d.bottom() - d.top())
                    width = (d.right() - d.left())
                    hh = int(height / 8)
                    ww = int(width / 8)
                    # 判断人脸是否超出 1280x960
                    if (d.right()+ww) > 1280 or (d.bottom()+hh > 960) or (d.left()-ww < 0) or (d.top()-hh < 0):
                        cv2.putText(frame, "OUT OF RANGE", (d.left(), d.bottom()), self.font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        color_rectangle = (0, 0, 255)
                        save_flag = 0
                        if kk == ord('s'):
                            logging.warning("Please adjust your position")
                    else:
                        color_rectangle = (255, 255, 255)
                        save_flag = 1
                    cv2.rectangle(frame,
                                  tuple([d.left() - ww, d.top() - hh]),
                                  tuple([d.right() + ww, d.bottom() + hh]),
                                  color_rectangle, 2)
                    # 根据人脸大小生成空的图像
                    img_blank = np.zeros((int(height + hh), width + ww, 3), np.uint8)
                    if save_flag:
                        # 按下 's' 保存人脸图像
                        if kk == ord('s'):
                            self.ss_cnt += 1
                            for ii in range(height + hh):
                                for jj in range(width + ww):
                                    img_blank[ii][jj] = frame[d.top()-hh + ii][d.left()-ww + jj]
                            cv2.imwrite(current_face_dir + "/img_face_" + str(self.ss_cnt) + ".jpg", img_blank)
                            logging.info("%-15s %s/img_face_%s.jpg", "Save into:",  str(current_face_dir), str(self.ss_cnt))
            # 按下 'ESC' 键退出
            if kk & 0xFF == 27:
                break
            cv2.namedWindow("Face Register", 1)
            cv2.imshow("Face Register",frame)
        # 释放摄像头并销毁所有窗口
        cap.release()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Face_Register = Face_Register()
    Face_Register.process()
