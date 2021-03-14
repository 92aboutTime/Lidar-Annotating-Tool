# Annotating Check Tools

### 환경설정



```python
import platform
print(platform.architecture())
```

확실하지 않지만 pyqt5는 32bit에서 실행이 되는거 같다.



### PyQT5 wikidocs

* https://wikidocs.net/21920

* 기초(basics)

  * 01) 창띄우기

    ```python
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget
    
    
    class MyApp(QWidget):
    
        def __init__(self):
            super().__init__()
            self.initUI()
    
        def initUI(self):
            self.setWindowTitle('My First Application')
            self.move(300, 300)
            self.resize(400, 200)
            self.show()
    
    
    if __name__ == '__main__':
       app = QApplication(sys.argv)
       ex = MyApp()
       sys.exit(app.exec_())
    ```

    위의 코드를 실행하면 아래와 같은 에러문이 나타난다.

    > File "c:/Users/dbtmd/Desktop/Lidar Labeling Tool/My First Application.py", line 2, in <module>
    >     from PyQt5.QtWidgets import QApplication, QWidget
    > ImportError: DLL load failed: 지정된 모듈을 찾을 수 없습니다.

    해결하기 위해서 참조한 싸이트 : 

    ​	https://www.inflearn.com/questions/116212

    ​	https://lazyquant.tistory.com/5?category=915088

    

    * 해결방법 시도 1:

      아나콘다에서 32bit 가상환경 만드는 방법을 알게 되었다.

      ```sh
      set CONDA_FORCE_32BIT = 1
      conda create -n qt python=3.6
      ```

      32bit로 가상환경을 만들었음에도 불구하고 계속 같은 에러문이 나타났다.

    

    * 해결방법 시도 2:

      https://stackoverflow.com/questions/42863505/dll-load-failed-when-importing-pyqt5/43045244#43045244

      ```sh
      pip install pyqt5
      ```

      pyqt5를 재설치하고 진행하니 아무 문제 없이 진행되었다.

