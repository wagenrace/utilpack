# -*- coding: utf-8 -*-
"""
===============================================
vis_util module
===============================================

========== ====================================
========== ====================================
 Module     vis_util module
 Date       2019-03-26
 Author     heewinkim
 Comment    `관련문서링크 <>`_
========== ====================================

*Abstract*
    * 데이터의 시각화 관련 유틸 모음

===============================================
"""


import matplotlib.pyplot as plt
import numpy as np
import cv2


class PyVisUtil(object):

    @staticmethod
    def color_hist(cv_img):
        """
        show color histogram on 2D plot

        :param cv_img:
        :return:None
        """

        chans = cv2.split(cv_img)
        colors = ("b", "g", "r")
        plt.figure()
        plt.title("Color Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixcels")
        features = []

        for (chan, color) in zip(chans, colors):
            hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
            features.extend(hist)

            plt.plot(hist, color=color)
            plt.xlim([0, 256])

        print("Flattened feature vector size: %d " % (np.array(features).flatten().shape))
        plt.show()

    @staticmethod
    def gray_hist(gray_img):
        """
        show gray histogram

        :param gray_img: cv gray image
        :return: None
        """

        hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        plt.figure()
        plt.title("Grayscale Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixcels")
        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()

    @staticmethod
    def pie(data, labels=None, title='', save_path=None, legend=True, radius=1, explode=0.05, shadow=True, colors=None,
            figsize=(8, 5), fontsize=12):
        """
        데이터의 파이를 그립니다.
        기본적으로 각 elelment의 percentage 및 개수를 표현하며, legend가 달립니다.
        ex. pie(data=[1,2,3],labels=['a','b','c'])

        :param data: 어떠한 데이터의 수량을 나타내는 리스트
        :param save_path: 경로 제공시 pie 이미지를 저장합니다.(eg. path/to/pie.png)
        :param title: 제목
        :param labels: 라벨 제공시 각 엘리먼트의 이름이 표시됩니다. 라벨은 데이터개수만큼의 문자요소 리스트 이어야 합니다.
        :param radius: default 1, matplotlib.pyplot.pie의 radius와 같습니다.
        :param explode: default 0.05, matplotlib.pyplot.pie의 요소와 같지만 리스트가 아닌 단일 float값을 받습니다.
        :param shadow: boolean 그림자 표시여부
        :param colors: default None, 각 요소의 색깔을 지정하고 싶을때 요소길이 만큼의 컬러가 주어져야합니다.
        :param figsize: figure size
        :param fontsize: element의 값을 표시하는 폰트의 크기
        :return:
        """

        data = list(data)
        labels = list(labels) if labels else None

        def label_func(percent, data):
            absolute = int(percent / 100. * np.sum(data))
            return "{:.1f}%\n({:d})".format(percent, absolute)

        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))

        if not labels:
            labels = [str(v) for v in data]

        wedges, texts, autotexts = ax.pie(
            data, autopct=lambda pct: label_func(pct, data), textprops=dict(color="w",fontsize=fontsize),
            radius=radius, explode=[explode] * len(data), shadow=shadow, colors=colors, labels=labels)

        if legend:
            ax.legend(wedges, labels, title="Label", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=fontsize, weight="bold")
        ax.set_title(title)
        if save_path:
            plt.savefig('{}'.format(save_path))
        plt.show()

    @staticmethod
    def plot3D(arr_list, label_list=None, figsize=(15, 15), colors=["#ff0000", "#0000ff", "#00ff00"],
               seperate_plot=False):
        from mpl_toolkits.mplot3d import Axes3D
        if not seperate_plot:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')

            ax.set_xlabel('x', fontsize=15)
            ax.set_ylabel('y', fontsize=15)
            ax.set_zlabel('z', fontsize=15)

            for i, data in enumerate(arr_list):
                ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colors[i % len(colors)], s=30)
            if label_list:
                ax.legend(label_list)
            else:
                ax.legend(['data{}'.format(i) for i in range(len(arr_list))])
            ax.grid()
        else:
            figsize = (list(figsize)[1] * len(arr_list), list(figsize)[1])
            fig = plt.figure(figsize=figsize)

            for i, data in enumerate(arr_list):
                ax = fig.add_subplot(1, len(arr_list), i + 1, projection='3d')

                ax.set_xlabel('x', fontsize=15)
                ax.set_ylabel('y', fontsize=15)
                ax.set_zlabel('z', fontsize=15)

                ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colors[i % len(colors)], s=30)

                if label_list:
                    ax.legend([label_list[i]])
                else:
                    ax.legend(['data{}'.format(i)])
                ax.grid()
        plt.show()


if __name__ == '__main__':

    img_cv = cv2.imread('/path/to/img.jpg')
    gray_img_cv = cv2.imread('/path/to/img.jpg',0)

    # 컬러 히스토그램을 그립니다.
    PyVisUtil.color_hist(img_cv)

    # 흑백 히스토그램을 그립니다.
    PyVisUtil.gray_hist(gray_img_cv)