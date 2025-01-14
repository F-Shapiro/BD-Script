# LogManager.py
from configparser import ConfigParser
import openpyxl
import pandas
import datetime
import os

config = ConfigParser()
config.read("config.ini")

class LogManager:
    __path = os.getcwd() + config["path"]["path_log"]
    __file_name = "load_log_" + datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + "_linux.xlsx"
    __dataframe = pandas.DataFrame({
    'Найденно товаров для обновления':[], #0
    'Скачанно':[], #1
    'Преобразованно':[], #2
    'Сохранены':[], #3
    'Обновленно в базе':[], #4
    'Ошибки для':[], #5
    'Время конца выполнения':[] #6
    })
    __step = [None for i in range(7)]
    __total = [None for i in range(7)]
    __number_row = 2
    __writer_mode = 'w'

    def __init__(self, count_steps):
        self.__count_steps = int(count_steps)
        self.__indexes = ["step " + str(i) for i in range(1, self.__count_steps+1)]
        self.__indexes.append("TOTAL")

    def writeLog(self):
        os.chmod(self.__path, 0o0777)
        with pandas.ExcelWriter(self.__path + f"/{self.__file_name}", mode=self.__writer_mode) as writer:
            if self.__writer_mode == 'w':
                self.__dataframe.to_excel(writer, sheet_name="convert_project")
                self.__writer_mode = 'a'
            else:
                book = openpyxl.load_workbook(self.__path + f"/{self.__file_name}")
                writer.book = book
                writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
                self.__dataframe.to_excel(writer, sheet_name="convert_project", header=False, startrow=self.__number_row)
                self.__number_row += 1
            writer.save()
        self.__dataframe = self.__dataframe.drop(index=self.__dataframe.index[0])
    
    def updateStep(self, data, index):
        self.__step[index] = data
        self.updateTotal(data, index)
    
    def updateTotal(self, data, index):
        if self.__total[index] is None:
            self.__total[index] = data
        else:
            self.__total[index] += data
    
    def writeFault(self, faultLog):
        if self.__step[len(self.__step)-2] is None:
            self.__step[len(self.__step)-2] = str(faultLog) + " "
        else:
            self.__step[len(self.__step)-2] += str(faultLog) + " "
    
    def addStepLog(self):
        self.__dataframe.loc[self.__indexes.pop(0)] = self.__step
        self.__step = [None for i in range(7)]
    
    def addTotalLog(self):
        self.__dataframe.loc[self.__indexes.pop(0)] = self.__total