#2.图像目标分割
import cv2
import matplotlib.pyplot as plt
import numpy as np

def main():
    # 1.导入图片
    img_src = cv2.imread('/home/mowen/4_python_test/test_4_7_files/20200128142556830.jpeg')
    # 2.转换为灰度图片
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img_src, cv2.COLOR_BGR2RGB)
    img_show = img_rgb.copy()
    # 3.二值化处理
    ret, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 4.执行开运算
    k = np.ones((3, 3), np.uint8)
    img_opening = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel=k, iterations=1)
    # 5.距离计算与前景剥离
    dist_transform = cv2.distanceTransform(img_opening, cv2.DIST_L2, 5)
    ret, img_fore = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, cv2.THRESH_BINARY)
    # 6.显示结果
    plt.figure("显示结果", figsize=(14, 10))
    plt.subplot(221)
    plt.imshow(img_show)
    plt.axis("off")
    plt.subplot(222)
    plt.imshow(img_bin, cmap="gray")
    plt.axis("off")
    plt.subplot(223)
    plt.imshow(dist_transform)
    plt.axis("off")
    plt.subplot(224)
    plt.imshow(img_fore)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    main()
cv2.destroyAllWindows()

