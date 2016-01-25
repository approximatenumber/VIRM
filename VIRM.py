#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
To move and rename files.
"""

import sys, os.path, shutil
from PyQt4 import QtGui, QtCore


class Mover(QtGui.QMainWindow):
    
    def __init__(self):
        super(Mover, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        def addClicked():
          global path
          path = QtGui.QFileDialog.getExistingDirectory(self, "Добавьте папку")
          sender = self.sender()							# узнать, что это делает
          if not path:
             self.statusBar().showMessage("Папка не выбрана")
          else:
             if not os.listdir(path):
               QtGui.QMessageBox.critical(None,'Ошибка',"Необходимые файлы отсутствуют", QtGui.QMessageBox.Close)
               sys.exit(app.exec_())
             else:
               btn_Run.setEnabled(True)
               self.statusBar().showMessage("Выбрана папка " + str(path))

        def runScript():
          export_dir = "exported"
          filenames = []
          for file in os.listdir(path):                           # make a list of files in the path
            if (os.path.isfile(os.path.join(path, file))) and ("." in file) and (len(', '.join(file.split('.')[:1])) >= 6):
              filenames.append(file)
          if not filenames:
            QtGui.QMessageBox.critical(None,'VIRM',"Необходимые файлы отсутствуют", QtGui.QMessageBox.Close)
            shutil.rmtree(path + "\\" + export_dir)
            sys.exit(app.exec_())
          if not os.path.isdir(path + "\\" + export_dir):
            os.makedirs(path + "\\" + export_dir)
          else:
            shutil.rmtree(path + "\\" + export_dir)
            os.makedirs(path + "\\" + export_dir)
          writelist = open(path + "\\" + export_dir + "\\" + "list.txt", "w")
          for filename in filenames:
                name = filename.split('.')[:1]                      
                name = ', '.join(name)                              # 465651039.dwg > 465651039
                name_part1 = name[0:6]                              # 465651039 > 465651
                if "_" in name:                                             # if 465257001ТУ_1
                  name_part2 = name.split('_')[:1]
                  name_part2 = ', '.join(name_part2)                        # 465257001ТУ_1 > 465257001ТУ
                  name_part2 = str(name_part2[6:])                          # 465257001ТУ > 001ТУ
                  change = name.split('_')[1:2]
                  change = ', '.join(change)                                # 465257001ТУ_1 > 1
                  new_dir = "ВМИР_%s_%s_ИЗМ%s" % (name_part1, name_part2, change)
                else:
                  name_part2 = name[6:]                             # 465651039 > 039
                  new_dir = "ВМИР_%s_%s" % (name_part1, name_part2)
                os.makedirs(path + "\\" + export_dir + "\\" + new_dir)
                shutil.copy(path + "\\" + filename, path + "\\" + export_dir + "\\" + new_dir + "\\" + filename)
                writelist.write("ВМИР.%s.%s\r\n" % (name_part1, name_part2))

          msgBox = QtGui.QMessageBox()
          msgBox.setText("Выполнено")
          msgBox.setWindowTitle("VIRM")
          self.statusBar().showMessage("Выполнено")
          btn_Run.setEnabled(False)
          msgBox.exec_()
          writelist.close()
        btn_ChoosePath = QtGui.QPushButton("Выбрать папку", self)
        btn_ChoosePath.setFixedWidth(150)
        btn_ChoosePath.move(100, 50)
        btn_ChoosePath.connect(btn_ChoosePath, QtCore.SIGNAL('clicked()'), addClicked)
        
        btn_Run = QtGui.QPushButton("Запустить", self)
        btn_Run.setFixedWidth(150)
        btn_Run.setEnabled(False)
        btn_Run.move(100, 100)
        btn_Run.connect(btn_Run, QtCore.SIGNAL('clicked()'), runScript)
        btn_Run.show()
        
        btn_Quit = QtGui.QPushButton("Выход", self)
        btn_Quit.setFixedWidth(80)
        btn_Quit.move(135, 150)
        btn_Quit.connect(btn_Quit, QtCore.SIGNAL('clicked()'), sys.exit)


        self.setGeometry(500, 500, 350, 300)
        self.setWindowTitle("VIRM. Very Insolent Renamer and Mover.")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.statusBar().showMessage("Выберите папку")
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Mover()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
