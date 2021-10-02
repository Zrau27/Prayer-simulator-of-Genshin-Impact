
import os
import random
import threading

from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie, QPixmap

import bottom_function as bf
import data as dt
from choose_track import track
from show_error import error
from main_ui import Ui_MainWindow

_translate = QtCore.QCoreApplication.translate



random.seed = "Genshin"
anystar = dt.strdata()

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.track_ui = track()
        self.error_ui = error()
        self.pushButton.clicked.connect(self.getten)
        self.pushButton_2.clicked.connect(self.getone)
        self.pushButton_3.clicked.connect(self.clear)
        self.pushButton_4.clicked.connect(self.showresults)
        self.pushButton_5.clicked.connect(self.deter_track)
        self.comboBox.currentIndexChanged.connect(self.cp_clear)        #combobox发生改变调用此函数
        self.track_ui.pushButton.clicked.connect(self.compare_track)

        self.fivestar_got = []   #记录已获得的五星
        self.fourstar_got = []   #记录已获得的四星
        self.lastgold = False    #记录上一发是否出金
        self.t = threading.Timer(0,self.show_pix,(os.getcwd()+'\\res\\temp\\0.png',))    #多线程计时器，若干秒后展示图片

        self.clear()      #初始化设置


#重置 或 跳过动画
    def clear(self):
        '''
        skip or clear
        '''
        #跳过祈愿动画
        if self.t.is_alive():     
            self.t.cancel()
            if self.status == 1:
                self.t = threading.Timer(0,self.show_pix,(os.getcwd()+'\\res\\temp\\0.png',))
            else:
                self.t = threading.Timer(0,self.show_pixs,(os.getcwd()+'\\res\\temp\\0.png',))
            self.t.start()
        
        #初始化
        else:
            self.total = 0              #五星(小)保底计数
            self.part = 0               #四星保底计数  
            self.count = 0              #总抽卡数 
            self.status = 1             #记录当前状态，1表示单抽，2表示十连抽
            self.fivestar_got = []      #记录得到的五星
            self.fourstar_got = []      #记录得到的四星
            self.lastgold = False       #记录上一发是否出金，第一次五星不重置四星保底，但第二次出四星或五星重置
                   
            choice = str(self.comboBox.currentText())              #读取下拉框选择哪个卡池
            self.ifup = [dt.judge_up(choice),False,False,0,0]      #数组ifup [卡池序号,四星大保底,五星大保底,武器池定轨选择,命定值]
            self.cardnum = dt.getnum(choice)                       #读取data中的数据，为卡池中物品数量信息
            self.show_bg(self.ifup[0])                             #展示背景图片

            self.specialnum = 0


#定义单抽函数
    def getone(self):
        '''
        pray once
        '''
        if self.t.is_alive():        #若在动画途中点击，取消之前结果的展示   
            self.t.cancel()      
        self.count += 1
        self.part += 1
        self.total += 1
        self.status = 1

        result = bf.getcards(self.total,self.part,self.ifup,self.cardnum)    #获取抽卡结果
        self.ifnextup(result)                          #对于up池，根据当前结果调整大保底计数
        result = dt.decoding(result,self.ifup[0])      #解码随机结果
        
        if result[0] == 4:    #抽到四星
            self.part = 0
            result_str = anystar[result[0]-3][result[1]][result[2]-1]
            self.fourstar_got.append(result_str)
            self.lastgold = False

        elif result[0] == 5:       #抽到五星
            result_str = anystar[result[0]-3][result[1]][result[2]-1]
            self.fivestar_got.append(result_str+"[{}]".format(self.total))
            if self.lastgold:
                self.total = 0
                self.part = 0
                self.lastgold = False
            else:
                self.total = 0
                self.lastgold = True

        elif result[0] == 3:               #抽到三星
            self.lastgold = False
        else:                            #报错
            print('something wrong in getone')

        self.show_result(result,6)      #展示结果

#定义十连抽函数
    def getten(self):
        '''
        pray ten times together
        '''
        if self.t.is_alive():     #若在动画途中点击，取消之前结果的展示  
            self.t.cancel()

        results = []            #保存十连结果
        maxstar = 4             #记录十连最大星数，决定抽卡动画
        self.status = 2
        for i in range(0,10):
            self.total += 1
            self.part += 1
            self.count += 1
            result = bf.getcards(self.total,self.part,self.ifup,self.cardnum)
            self.ifnextup(result)
            result = dt.decoding(result,self.ifup[0])

            if result[0] == 4:
                self.part = 0
                result_str = anystar[result[0]-3][result[1]][result[2]-1]
                self.fourstar_got.append(result_str)
                self.lastgold = False
                results.append(result)
            
            elif result[0] == 5:
                maxstar = 5
                result_str = anystar[result[0]-3][result[1]][result[2]-1]
                self.fivestar_got.append(result_str+"[{}]".format(self.total))
                results.append(result)
                if self.lastgold:
                    self.total = 0
                    self.part = 0
                    self.lastgold = False
                else:
                    self.total = 0
                    self.lastgold = True
                
            elif result[0] == 3:
                self.lastgold = False
                results.append(result)
            else:
                print("someting error in getten")
        
        self.show_results(results,maxstar,6)

#展示统计结果
    def showresults(self):      
        '''
        show all results (5stars, 4stars)
        '''    
        if self.t.is_alive():
            self.t.cancel()
        self.label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        four_list = self.statistics(self.fourstar_got)
        fivestar_got_str = " ".join(self.fivestar_got)
        fourstar_got_str = " ".join(four_list)
        self.label.setText(
            "<font color = black face = '宋体' size=5>总抽卡数:{}<font><br>".format(self.count)+
            "<font color = black face = '宋体' size=5>距上次保底已抽:{}<font><br>".format(self.total)+
            "<font color = black face = '宋体' size=5>抽到的五星数:{}<font><br>".format(len(self.fivestar_got))+
            "<font color = orange face = '宋体' size=5>{}<font><br>".format(fivestar_got_str)+
            "<font color = black face = '宋体' size=5>抽到的四星数:{}<font><br>".format(len(self.fourstar_got))+
            "<font color = purple face = '宋体' size=5>{}<font>".format(fourstar_got_str)
        )


#组件函数
#展示结果动画（蓝、紫、金光）
    def show_gif(self,fname):
        '''
        show the gif before the result
        not good gif
        '''
        path = os.getcwd()+"\\res\\preview\\{}.gif".format(fname)
        movie = QMovie(path)
        movie.setSpeed(100)
        self.label.setScaledContents(True)     #占满label
        self.label.setMovie(movie)
        movie.start()
        
#展示单抽结果图片
    def show_pix(self,path):
        '''
        show the picture of one card
        '''
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        pix = QPixmap(path)
        self.label.setPixmap(pix)
        self.pushButton_3.setText(_translate("Mainwindow","重置"))

#根据结果获取路径
    def get_path(self,result):
        '''
        result: a tuple  ->  (star3/4/5, char0/arms1, order)
        return the path corresponding to the result
        '''
        root = os.path.dirname(os.path.abspath(sys.argv[0]))
        path = os.path.join(root, 'res\\%d%d'%(result[0],result[1])+'\\{}.png'.format(result[2]))
        return path

#展示单抽结果
    def show_result(self,result,sleeptime):
        '''
        show the result of getting one card
        '''
        path = self.get_path(result)
        img = Image.open(path)
        path2 = os.getcwd()+'\\res\\temp\\0.png'
        img.save(path2)
        self.show_gif(result[0]-2)
       
        self.t = threading.Timer(sleeptime,self.show_pix,(path2,))
        self.t.start() 

        self.pushButton_3.setText(_translate("MainWindow", "跳过"))
        
  
#合并图片
    def package_imgs(self,results):
        '''
        results: the result of getting ten cards together, it's a list with 10 tuples
        Merge ten pictures into one big picture in the form of 5*2
        return the path of the big picture
        '''
        to_img = Image.new('RGB',(132*5-4,160*2-4))
        k = 0
        for y in range(0,2):
            for x in range(0,5):
                #print(results[k])
                img = Image.open(self.get_path(results[k]))
                k+=1
                to_img.paste(img,(x*132,y*160))
                img.close()
        path = os.getcwd()+'\\res\\temp\\0.png'
        to_img.save(path)
        return path

#展示大图片
    def show_pixs(self,path):
        '''
        path: the path of the big picture
        show the big picture in ui
        '''
        self.label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setScaledContents(True)
        pix = QPixmap(path)
        self.label.setPixmap(pix)
        self.pushButton_3.setText(_translate("Mainwindow","重置"))

#展示十连结果
    def show_results(self,results,maxstar,sleeptime):
        '''
        show the results in ui 
        '''
        path = self.package_imgs(results)
        self.show_gif(maxstar)
        
        self.t = threading.Timer(sleeptime,self.show_pixs,(path,))
        self.t.start()   
        self.pushButton_3.setText(_translate("MainWindow", "跳过"))
    

#调整大保底计数
    def ifnextup(self,result):
        
        if self.ifup[0] != 0:               #普通大保底
            if result[2]>0:
                if result[0] == 4:
                    self.ifup[1] = True
                elif result[0] == 5:
                    self.ifup[2] = True
            elif result[2]<0:
                if result[0] == 4:
                    self.ifup[1] = False
                elif result[0] == 5:
                    self.ifup[2] = False
        
        if self.ifup[3] < 0 and result[0]==5:       #武器池定轨
            if self.ifup[3] != result[2]:
                self.ifup[4] = self.ifup[4]+1
            else:
                self.ifup[4] = 0

#切换池子后，初始化
    def cp_clear(self):
        '''
        when change the pool, clear
        '''
        if self.t.is_alive():
            self.t.cancel()
        
        self.total = 0
        self.part = 0
        self.count = 0
        self.fivestar_got = []
        self.fourstar_got = []
        self.lastgold = False
        choice = str(self.comboBox.currentText())
        self.ifup = [dt.judge_up(choice),False,False,0,0]
        self.cardnum = dt.getnum(choice)
        self.show_bg(self.ifup[0])
        self.specialnum = 0

#打开定轨选择窗口
    def deter_track(self):
        '''
        open the track window
        '''
        if self.ifup[0]<0:
            uparms = dt.up_arms(self.ifup[0])
            self.track_ui.radioButton.setText(uparms[0])
            self.track_ui.radioButton_2.setText(uparms[1])
            self.track_ui.show()
        else:
            #彩蛋 colorful_egg
            specialtext = ["抱歉!该卡池无定轨玩法","再点一下试试？","再点一下？","再点一下","再点一下"]
            if self.specialnum < 5:
                self.error_ui.raise_error(specialtext[self.specialnum])
                self.error_ui.show()
                
            elif self.specialnum <= 8:
                self.show_pixs(os.getcwd()+"\\res\\special\\{}.jpg".format(5-self.specialnum))
            else:
                self.show_pixs(os.getcwd()+"\\res\\special\\{}.jpg".format(self.specialnum-8))
            if self.specialnum >= 127:
                self.specialnum = 8
            self.specialnum = self.specialnum + 1

#读取定轨选择结果
    def compare_track(self):
        '''
        get the choice of track
        '''
        if self.ifup[0] < 0:
            if self.ifup[3] != self.track_ui.track:
                self.ifup[3] = self.track_ui.track
                self.ifup[4] = 0
        self.track_ui.close()

#展示背景图片
    def show_bg(self,n):
        '''
        show background
        '''
        path1 = os.getcwd()+'\\res\\bg\\{}.png'.format(n)
        path2 = os.getcwd()+'\\res\\bg\\{}.jpeg'.format(n)
        if os.path.exists(path1):
            self.show_pixs(path1)
        elif os.path.exists(path2):
            self.show_pixs(path2)

#统计结果
    def statistics(self,got):
        '''
        statisticsthe result
        return a dict
        '''
        dic = {}
        for i in got:
            if i in dic:
                dic[i] = dic[i]+1
            else:
                dic[i] = 1
        l = dic.items()
        res_list = []
        for i in l:
            if i[1] > 1:
                res_list.append(i[0]+"({})".format(i[1]))
            else:
                res_list.append(i[0])
        return res_list

        


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    sys.exit(app.exec_())
