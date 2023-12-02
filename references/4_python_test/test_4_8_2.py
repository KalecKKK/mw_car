#2、人脸特征提取
import numpy as np
import cv2
import os
import csv
import logging
import dlib
# 待读取人脸图像文件的路径
path_images_from_camera = "test_4_8_data/data_faces/"
# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()
# Dlib 人脸 landmark 特征点检测器
predictor = dlib.shape_predictor('test_4_8_data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet 人脸识别模型，提取 128D 的特征矢量
face_reco_model = dlib.face_recognition_model_v1("test_4_8_data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")
# 返回单张图像的 128D 特征
def return_128d_features(path_img):
    img_rd = cv2.imread(path_img)
    faces = detector(img_rd, 1)
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
        logging.info("%-30s %-20s", "Image with faces detected:", path_img)
    else:
        face_descriptor = 0
        logging.warning("no face")
    return face_descriptor
# 返回某人的 128D 特征均值
def return_features_mean_personX(path_face_personX):
    features_list_personX = []
    photos_list = os.listdir(path_face_personX)
    if photos_list:
        for i in range(len(photos_list)):
            logging.info("%-30s %-20s", "Reading image:", path_face_personX + "/" + photos_list[i])
            features_128d = return_128d_features(path_face_personX + "/" + photos_list[i])
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        logging.warning("Warning: No images in%s/", path_face_personX)
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX, dtype=object).mean(axis=0)
    else:
        features_mean_personX = np.zeros(128, dtype=object, order='C')
    return features_mean_personX
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    person_list = os.listdir("test_4_8_data/data_faces/")
    person_list.sort()
    with open("test_4_8_data/faces_features.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for person in person_list:
            logging.info("%s%s", path_images_from_camera, person)
            features_mean_personX = return_features_mean_personX(path_images_from_camera + person)
            features_mean_personX = np.insert(features_mean_personX, 0, person, axis=0)
            writer.writerow(features_mean_personX)
            logging.info('\n')
        logging.info("Save all the features of faces registered into: test_4_8_data/faces_features.csv")
