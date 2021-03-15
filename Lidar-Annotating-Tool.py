import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import os

class LidarAnnotatingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def make_label_list(self, fname):
        # QFileDialog에서 얻은 fname을 통해 label_list를 만드는 함수.
        label_list = os.listdir(os.path.join(fname, 'lidar', 'lidar_label'))
        return label_list

    def initUI(self):
        # 처음에 폴더를 여는 과정 및 첫번째 layout에 들어가는 folder_Qlabel 선언하는 과정
        fname = QFileDialog.getExistingDirectory(self, 'Select a directory', './')
        # fname == C:/Users/wq_ysw/Desktop/Project/Lidar-Annotating-Tool/mkdown
        folder_Qlabel = QLabel(fname.split("/")[-1])
        folder_Qlabel_font = folder_Qlabel.font()
        folder_Qlabel_font.setPointSize(15) # 글자크기
        folder_Qlabel_font.setBold(True)
        folder_Qlabel.setFont(folder_Qlabel_font)


        # 첫번째 layout에 들어가는 combobox에 필요한 label_list를 가져오는 과정 및 combobox 선언하는 과정
        label_Combobox = QComboBox(self)
        label_list = sorted(self.make_label_list(fname))
        for label in label_list:
            label_Combobox.addItem(label)


        # 첫번째 layout은 수평으로 되어 있으며, folder_Qlabel과 label_Combobox로 이루어짐.
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(folder_Qlabel)
        hbox_1.addWidget(label_Combobox)
        

        # QTableWidget으로 테이블이 들어감.
        table = QTableWidget(self)
        table.setColumnCount(7)
        table.setRowCount(40)
        table.setHorizontalHeaderLabels(
            ['tracking ID', 'Height(m)', 'Point Cloud', '동일 ID 유무', '높이 차이(m)', '전프레임과 Type 다름', '전프레임과 거리(m)']
            )
        # QTable 배경색 지정하는 방법 : https://alwaysemmyhopes.com/ko/python/715989-how-i-can-change-the-background-color-in-qtablewidget-duplicate-python-pyqt-pyside.html
        # QTable 글자 수정 못하게 하는 방법 : https://m.blog.naver.com/PostView.nhn?blogId=thenaru2&logNo=220788804430&proxyReferer=https:%2F%2Fwww.google.com%2F
        # QTableWidget : https://wikidocs.net/36797
        # 백그라운드 속성 : https://wikidocs.net/37096

        # 두번째 layout에 들어가는 다시읽기 버튼을 선언하는 과정
        btn_1 = QPushButton("&1_다시 읽기", self) # 단축키 선언하는 방법이 있다.
        btn_1.toggle()


        # 두번째 layout에 들어가는 다시읽기 버튼을 선언하는 과정
        btn_2 = QPushButton("&2_폴더에서 동일 bounding box 지우기", self) # 단축키 선언하는 방법이 있다.
        btn_2.toggle()


        # 두번째 layout은 수평으로 되어 있으며, 다시읽기 버튼과 폴더에서 동일 bounding box 지우기 버튼으로 구성됨.
        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(btn_1)
        hbox_2.addWidget(btn_2)


        # 세번째 layout에 들어가는 제한높이 설정 QSpinBOX를 선언하는 과정
        self.limit_height_QLabel = QLabel('제한 높이')
        self.limit_height_spinBox = QSpinBox()
        self.limit_height_spinBox.setMinimum(1)
        self.limit_height_spinBox.setMaximum(4)
        self.limit_height_spinBox.setSingleStep(0.1)


        # 세번째 layout에 들어가는 제한 PointCloud 갯수를 설정하는 QSpinBOX를 선언하는 과정
        self.limit_point_cloud_QLabel = QLabel('제한 Point Cloud')
        self.limit_point_cloud = QSpinBox()
        self.limit_point_cloud.setMinimum(0)
        self.limit_point_cloud.setMaximum(20)
        self.limit_point_cloud.setSingleStep(1)
        

        # 세번째 layout에 들어가는 높이차이 제한 설정하는 QSpinBOX를 선언하는 과정
        self.limit_gap_height_QLabel = QLabel('제한 높이 차이')
        self.limit_gap_height = QSpinBox()
        self.limit_gap_height.setMinimum(0)
        self.limit_gap_height.setMaximum(2)
        self.limit_gap_height.setSingleStep(0.1)
        

        # 세번째 layout에 들어가는 거리제한 설정하는 QSpinBOX를 선언하는 과정
        self.limit_distance_QLabel = QLabel('제한 거리')
        self.limit_distance = QSpinBox()
        self.limit_distance.setMinimum(0)
        self.limit_distance.setMaximum(100)
        self.limit_distance.setSingleStep(1)
        

        hbox_3 = QHBoxLayout()
        hbox_3.addStretch(1)
        hbox_3.addWidget(self.limit_height_QLabel)
        hbox_3.addWidget(self.limit_height_spinBox)
        hbox_3.addStretch(1)
        hbox_3.addWidget(self.limit_point_cloud_QLabel)
        hbox_3.addWidget(self.limit_point_cloud)
        hbox_3.addStretch(1)
        hbox_3.addWidget(self.limit_gap_height_QLabel)
        hbox_3.addWidget(self.limit_gap_height)
        hbox_3.addStretch(1)
        hbox_3.addWidget(self.limit_distance_QLabel)
        hbox_3.addWidget(self.limit_distance)
        hbox_3.addStretch(1)

        # 마지막에 모든 레이어를 넣어주는 과정이 필요하다.
        vbox = QVBoxLayout() # 제일 마지막에 hbox들을 넣어준다.
        vbox.addLayout(hbox_1)
        vbox.addWidget(table)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)
        self.setWindowTitle('Lidar-Annotating-Tool')
        self.move(0, 0)
        self.resize(770, 820)
        self.setLayout(vbox)
        self.show()


if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = LidarAnnotatingTool()
    sys.exit(app.exec_())