import numpy as np
import cv2
import os
import pandas
import logging
import dlib

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸 landmark 特征点检测器
predictor = dlib.shape_predictor('test_4_8_data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib ResNet 人脸识别模型, 提取 128D 的特征矢量
face_reco_model = dlib.face_recognition_model_v1("test_4_8_data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


class Face_Recognizer:
    def __init__(self):
        self.font = cv2.FONT_ITALIC


        self.face_name_known_list = []         # 存放已录入 人脸的 名字
        self.face_features_known_list = []     # 存放已录入 人脸特征的 数组

        # 存放上一帧和当前帧中捕获到的 人脸数
        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        # 如果识别出 " " 的脸, 将在 reclassify_interval_cnt 计数到 reclassify_interval 后, 对当前帧人脸进行再识别
        self.reclassify_interval_cnt = 0
        self.reclassify_interval = 2

        # 存放当前帧中捕获到的 人脸特征
        self.current_frame_face_feature_list = []

        # 存放当前帧中捕获到的 所有人脸的名字 的坐标
        self.current_frame_face_name_position_list = []

        # 存放上一帧和当前帧中捕获到的 所有人脸的名字
        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []

        # 存放上一帧和当前帧 ROI 的质心坐标
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        # 上一帧和当前帧 ROI 质心的欧氏距离
        self.last_current_frame_centroid_e_distance = 0


        # 存放当前帧中 X相对库里人脸的欧氏距离
        self.current_frame_face_X_e_distance_list = []

    # 从 "faces_features.csv" 读取已录入人脸特征
    def get_face_database(self):
        if os.path.exists("test_4_8_data/faces_features.csv"):
            path_features_known_csv = "test_4_8_data/faces_features.csv"
            csv_rd = pandas.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                for j in range(1, 129):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            logging.info("Faces in Database： %d", len(self.face_features_known_list))
            return 1
        else:
            logging.warning("'faces_features.csv' not found!")
            logging.warning("Please run 'test_4_8_1.py'"
                            "and 'test_4_8_2.py' before 'test_4_8_3.py'")
            return 0

    @staticmethod
    # 计算两个 128D 向量间的欧式距离
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist
    # 使用 质心追踪 来识别人脸
    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])
                e_distance_current_frame_person_x_list.append(self.last_current_frame_centroid_e_distance)

            last_frame_num = e_distance_current_frame_person_x_list.index(min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]

    # 在人脸框下面显示人名
    def draw_name(self, img_rd):
        for i in range(self.current_frame_face_cnt):
            cv2.putText(img_rd, self.current_frame_face_name_list[i],
                        self.current_frame_face_name_position_list[i],
                        self.font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        return img_rd

    # 处理获取的视频流, 并进行人脸识别
    def process(self):
        # 从 "faces_features.csv" 读取已录入的人脸特征
        if self.get_face_database():
            # 配置流式传输的管道
            cap = cv2.VideoCapture(0)

            
            while True:
                ret,frame = cap.read()
                kk = cv2.waitKey(1)
                faces = detector(frame, 0)   

                # 更新上一帧和当前帧中捕获到的 人脸数
                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)         # 值后更新

                # 更新上一帧中捕获到的 所有人脸的名字
                self.last_frame_face_name_list = self.current_frame_face_name_list[:]

                # 更新上一帧和当前帧 ROI 的质心坐标
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

                # 如果当前帧和上一帧人脸数没有变化
                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (self.reclassify_interval_cnt != self.reclassify_interval):
                    logging.debug("scene 1: 当前帧和上一帧相比没有发生人脸数变化")
                    self.current_frame_face_name_position_list = []

                    if " " in self.current_frame_face_name_list:
                        logging.debug("有未知人脸, 开始进行 reclassify_interval_cnt 计数")
                        self.reclassify_interval_cnt += 1

                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            # print(d)
                            self.current_frame_face_name_position_list.append(tuple([faces[k].left(), int(faces[k].bottom() + 25)]))
                            self.current_frame_face_centroid_list.append([int(faces[k].left() + faces[k].right()) / 2, int(faces[k].top() + faces[k].bottom()) / 2])

                            cv2.rectangle(frame, tuple([d.left(), d.top()]),  tuple([d.right(), d.bottom()]),  (255, 255, 255), 2)

                    # 如果当前帧中有多个人脸, 使用质心追踪
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()

                    # 在人脸框下面显示人名
                    frame = self.draw_name(frame)

                # 如果当前帧和上一帧人脸数发生变化
                else:
                    logging.debug("scene 2: 当前帧和上一帧相比人脸数发生变化")
                    self.current_frame_face_name_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    # 人脸数减少
                    if self.current_frame_face_cnt == 0:
                        logging.debug("scene 2.1 人脸消失, 当前帧中没有人脸")
                        self.current_frame_face_name_list = []        # 清空列表
                    # 人脸数增加
                    else:
                        logging.debug("scene 2.2 出现人脸, 进行人脸识别")
                        self.current_frame_face_name_list = []
                        for i in range(len(faces)):
                            shape = predictor(frame, faces[i])
                            self.current_frame_face_feature_list.append(face_reco_model.compute_face_descriptor(frame, shape))
                            self.current_frame_face_name_list.append(" ")

                        # 遍历捕获到的图像中所有的人脸
                        for k in range(len(faces)):
                            logging.debug("For face %d in current frame:", k + 1)
                            self.current_frame_face_centroid_list.append([int(faces[k].left() + faces[k].right()) / 2,
                                                                          int(faces[k].top() + faces[k].bottom()) / 2])

                            self.current_frame_face_X_e_distance_list = []

                            # 当前帧中捕获到的 所有人脸的名字 的坐标
                            self.current_frame_face_name_position_list.append(tuple([faces[k].left(), int(faces[k].bottom() + 25)]))

                            # 对于某张人脸, 遍历所有存储的人脸特征
                            for i in range(len(self.face_features_known_list)):
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    e_distance_tmp = self.return_euclidean_distance(self.current_frame_face_feature_list[k],
                                                                                    self.face_features_known_list[i])
                                    logging.debug("with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                else:
                                    self.current_frame_face_X_e_distance_list.append(999999999)

                            # 寻找出最小的欧式距离匹配
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(min(self.current_frame_face_X_e_distance_list))

                            if min(self.current_frame_face_X_e_distance_list) < 0.4:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                                logging.debug("Face recognition result: %s", self.face_name_known_list[similar_person_num])
                            else:
                                logging.debug("Face recognition result: Unknown person")

                        # 在人脸框下面显示人名
                        frame = self.draw_name(frame)

                # 按下 'ESC' 键（退出while），退出人脸识别
                kk = cv2.waitKey(1)
                if kk & 0xFF == 27:
                    break

                cv2.namedWindow("Face Recognizer", 1)
                cv2.imshow("Face Recognizer", frame)
                logging.debug("Frame ends\n\n")

            # 释放摄像头并销毁所有窗口
            cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    Face_Recognition = Face_Recognizer()
    Face_Recognition.process()
