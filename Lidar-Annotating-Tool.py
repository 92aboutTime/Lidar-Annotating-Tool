import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import os

basic_DataFrame_columns = ['']
DataFrame_columns = ['tracking ID', 'Height(m)', 'Point Cloud', '동일 ID 유무', '높이 차이(m)', '전프레임과 Type 다름', '전프레임과 거리(m)']

class LidarAnnotatingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.read_lines = [] # QCombobox에서 어떠한 txt를 선택할 경우 txt 파일을 readlines한 결과
        self.basic_DataFrame = None

        # 처음에 폴더를 여는 과정 및 첫번째 layout에 들어가는 self.folder_Qlabel 선언하는 과정
        self.fname = QFileDialog.getExistingDirectory(self, 'Select a directory', './')
        self.fname = self.fname.replace('/','\\')

        # fname == C:/Users/wq_ysw/Desktop/Project/Lidar-Annotating-Tool/
        self.folder_Qlabel = QLabel(self.fname.split("/")[-1])
        self.folder_Qlabel_font = self.folder_Qlabel.font()
        self.folder_Qlabel_font.setPointSize(15) # 글자크기
        self.folder_Qlabel_font.setBold(True)
        self.folder_Qlabel.setFont(self.folder_Qlabel_font)


        # 첫번째 layout에 들어가는 combobox에 필요한 label_list를 가져오는 과정 및 combobox 선언하는 과정
        self.label_Combobox = QComboBox(self)
        self.label_list = sorted(self.make_label_list(self.fname))
        for label in self.label_list:
            self.label_Combobox.addItem(label)

        self.read_txt()
         
        self.label_Combobox.currentIndexChanged.connect(self.read_txt) # 클릭하면 self.read_text 함수 실행하는 부분.

        # 어떤 함수를 만들어서. self.read_text(), self.make_basic_DataFrame(), self.make_DataFrame() 함수를 실행한다.
        # 실행한 후, QTablewidget 생성 후, 값을 옮겨 담는다.
        # 그 다음, QTable 값을 변경하지 못하게 하고, 버튼으로만 변경할 수 있게 한다.
        # 특정 조건들에 걸리면 QTabelwidget에서 글자, 배경의 색깔을 변경하는 것을 만든다.
        # 만약 수정했을 경우, 수정하는 버튼도 만들어야 한다. 
        #   우선 수정하는 버튼은 만들지 말고, 수정은 우선 PCL을 모두 사용하여, pointcloud를 보이게 만든 후, 생각한다. 


        # 첫번째 layout은 수평으로 되어 있으며, self.folder_Qlabel과 self.label_Combobox로 이루어짐.
        self.hbox_1 = QHBoxLayout()
        self.hbox_1.addWidget(self.folder_Qlabel)
        self.hbox_1.addWidget(self.label_Combobox)
        
        # QTableWidget으로 테이블이 들어감.
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setRowCount(40)
        self.table.setHorizontalHeaderLabels(
            DataFrame_columns
            )
        # QTable 배경색 지정하는 방법 : https://alwaysemmyhopes.com/ko/python/715989-how-i-can-change-the-background-color-in-qtablewidget-duplicate-python-pyqt-pyside.html
        # QTable 글자 수정 못하게 하는 방법 : https://m.blog.naver.com/PostView.nhn?blogId=thenaru2&logNo=220788804430&proxyReferer=https:%2F%2Fwww.google.com%2F
        # QTableWidget : https://wikidocs.net/36797
        # 백그라운드 속성 : https://wikidocs.net/37096

        # 두번째 layout에 들어가는 다시읽기 버튼을 선언하는 과정
        self.btn_1 = QPushButton("&1_다시 읽기", self) # 단축키 선언하는 방법이 있다.
        self.btn_1.toggle()


        # 두번째 layout에 들어가는 다시읽기 버튼을 선언하는 과정
        self.btn_2 = QPushButton("&2_폴더에서 동일 bounding box 지우기", self) # 단축키 선언하는 방법이 있다.
        self.btn_2.toggle()


        # 두번째 layout은 수평으로 되어 있으며, 다시읽기 버튼과 폴더에서 동일 bounding box 지우기 버튼으로 구성됨.
        self.hbox_2 = QHBoxLayout()
        self.hbox_2.addWidget(self.btn_1)
        self.hbox_2.addWidget(self.btn_2)


        # 세번째 layout에 들어가는 제한높이 설정 QSpinBOX를 선언하는 과정
        self.limit_height_QLabel = QLabel('제한 높이')
        self.limit_height_spinBox = QSpinBox()
        self.limit_height_spinBox.setMinimum(1)
        self.limit_height_spinBox.setMaximum(4)
        self.limit_height_spinBox.setSingleStep(1)


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
        self.limit_gap_height.setSingleStep(1)
        

        # 세번째 layout에 들어가는 거리제한 설정하는 QSpinBOX를 선언하는 과정
        self.limit_distance_QLabel = QLabel('제한 거리')
        self.limit_distance = QSpinBox()
        self.limit_distance.setMinimum(0)
        self.limit_distance.setMaximum(100)
        self.limit_distance.setSingleStep(1)
        

        self.hbox_3 = QHBoxLayout()
        self.hbox_3.addStretch(1)
        self.hbox_3.addWidget(self.limit_height_QLabel)
        self.hbox_3.addWidget(self.limit_height_spinBox)
        self.hbox_3.addStretch(1)
        self.hbox_3.addWidget(self.limit_point_cloud_QLabel)
        self.hbox_3.addWidget(self.limit_point_cloud)
        self.hbox_3.addStretch(1)
        self.hbox_3.addWidget(self.limit_gap_height_QLabel)
        self.hbox_3.addWidget(self.limit_gap_height)
        self.hbox_3.addStretch(1)
        self.hbox_3.addWidget(self.limit_distance_QLabel)
        self.hbox_3.addWidget(self.limit_distance)
        self.hbox_3.addStretch(1)

        # 마지막에 모든 레이어를 넣어주는 과정이 필요하다.
        self.vbox = QVBoxLayout() # 제일 마지막에 hbox들을 넣어준다.
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addWidget(self.table)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox_3)
        self.setWindowTitle('Lidar-Annotating-Tool')
        self.move(0, 0)
        self.resize(770, 820)
        self.setLayout(self.vbox)

        
        self.show()

    def make_basic_DataFrame(self):
        self.basic_DataFrame = pd.DataFrame(self.read_lines, column = basic_DataFrame_columns)


    def make_DataFrame(self):
        a = 0

    def make_label_list(self, fname):
        # QFileDialog에서 얻은 fname을 통해 label_list를 만드는 함수.
        label_list = os.listdir(os.path.join(fname, 'lidar', 'lidar_label'))
        return label_list
    
    def read_txt(self):
        txt = self.label_Combobox.currentText()
        txt_path = os.path.join(self.fname, "lidar", "lidar_label", txt)

        with open(txt_path, 'r') as f:
            readlines = f.readlines()
            for i, line in enumerate(readlines):
                readlines[i] = line.replace("\n", "")
            self.read_lines = readlines



        


if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = LidarAnnotatingTool()
    sys.exit(app.exec_())