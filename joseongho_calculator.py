import traceback
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QThread


from_class = uic.loadUiType("/home/jo/dev_ws/PyQt/Source/pyqt5/calculator.ui")[0]


class MyCalculator(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Joseongho's Carculator")

        self.default_display = ""
        self.input_line.setText(self.default_display)

        self.error_list = ['-0.09999999999999998']
        self.four_base = ['+', '−', '×', '÷']

        self.num_0.clicked.connect(lambda:self.number_Clicked(0))
        self.num_1.clicked.connect(lambda:self.number_Clicked(1))
        self.num_2.clicked.connect(lambda:self.number_Clicked(2))
        self.num_3.clicked.connect(lambda:self.number_Clicked(3))
        self.num_4.clicked.connect(lambda:self.number_Clicked(4))
        self.num_5.clicked.connect(lambda:self.number_Clicked(5))
        self.num_6.clicked.connect(lambda:self.number_Clicked(6))
        self.num_7.clicked.connect(lambda:self.number_Clicked(7))
        self.num_8.clicked.connect(lambda:self.number_Clicked(8))
        self.num_9.clicked.connect(lambda:self.number_Clicked(9))


        self.point.clicked.connect(lambda:self.point_Clicked('.'))


        self.plus.clicked.connect(lambda:self.operation_Clicked('+'))
        self.minus.clicked.connect(lambda:self.operation_Clicked('−'))
        self.product.clicked.connect(lambda:self.operation_Clicked('×'))
        self.division.clicked.connect(lambda:self.operation_Clicked('÷'))


        self.enter.clicked.connect(self.enter_Clicked)


        self.open_paren.clicked.connect(lambda:self.equation_Clicked('('))
        self.close_paren.clicked.connect(lambda:self.equation_Clicked(')'))
        self.squre.clicked.connect(lambda:self.equation_Clicked('²'))
        self.root.clicked.connect(lambda:self.equation_Clicked('√'))


        self.backSpace.clicked.connect(self.backSpace_Clicked)
        self.cancel.clicked.connect(self.remove_all)

        

    def number_Clicked(self, num):
        self.error_line.clear()
        if self.input_line.text() == self.default_display or self.input_line.text() == '0':
            display = ''
        else:
            display = self.input_line.text()


        # 개선사항 1 23.10.11
        if len(display) >= 1:
            if display[-1] == '²':
                self.error_line.setText("연산자를 먼저 사용해주세요.")
            elif display[-1] == ')':
                display = display + '×' + str(num)
            else:
                display += str(num)
        else:
            display += str(num)

        self.input_line.setText(display)

    
    def point_Clicked(self, point):
        self.error_line.clear()
        if self.input_line.text() == self.default_display:
            display = '0'
        else:
            display = self.input_line.text()

        # 개선사항 2 : 소수점 연속사용 금지 23.10.11
        count = 0
        for i in display[::-1]:
            if i.isdigit():
                pass
            elif i == '.':
                count += 1
            else:
                break
        
        if count == 0:
            display += str(point)
        else:
            self.error_line.setText("더이상 소수점을 사용할수 없습니다.")
        self.input_line.setText(display)

        
    def operation_Clicked(self, oper):
        self.error_line.clear()
        if self.input_line.text() == self.default_display:
            display = ''
        else:
            display = self.input_line.text()

       
        if len(display) >= 1 and display[-1] == '.':
            self.error_line.setText("소수점 뒤에 연산자를 사용할 수 없습니다.")

        elif str(oper) == '×':
            if len(display) == 0:
                self.error_line.setText("곱셈 연산자를 사용할수 없습니다.")
            else:
                if display[-1] in self.four_base:
                    self.error_line.setText("이전연산자와 연속해서 사용할 수 없습니다.")
                elif display[-1] == '(':
                    self.error_line.setText("개괄호 바로 다음으로 사용할 수 없습니다.")
                else:
                    display += str(oper)

        elif str(oper) == '÷':
            if len(display) == 0:
                self.error_line.setText("나눗셈 연산자를 사용할수 없습니다.")
            else:
                if display[-1] in self.four_base:
                    self.error_line.setText("이전연산자와 연속해서 사용할 수 없습니다.")
                elif display[-1] == '(':
                    self.error_line.setText("개괄호 바로 다음으로 사용할 수 없습니다.")
                else:
                    display += str(oper)

        else:
            count = 0
            if len(display) >= 1:
                for i in display[:len(display)-3:-1]:
                    if i in self.four_base:
                        count += 1
                    else:
                        count = count
            if count < 2:
                display += str(oper)
            else:
                self.error_line.setText("연산자는 3개를 연속으로 사용할 수 없습니다.")
        
        self.input_line.setText(display)


    def enter_Clicked(self):
        try:
            previous_display = self.display_line.toPlainText()
            if self.input_line.text() == self.default_display:
                display = '0'
            else:
                mathmetical = self.calculation()
                calc = eval(mathmetical)

            if len(str(calc)) <= 10:
                display = str(calc)
                
            else:
                if str(calc) in self.error_list:
                    display = str(format(calc, '.1f'))

                else:
                    display = str(format(calc, 'e'))


            if self.error_line.text() == '':
                pass
            else:
                self.error_line.clear()

            self.input_line.clear()
            self.input_line.setText(display)
            self.display_line.setText(previous_display + '\n' + mathmetical + '\n' \
                                        + display.rstrip() + '\n' + '----------------------------')
        
        except:
            display = self.input_line.text()
            err_msg = traceback.format_exc()

            for error in self.error_list:
                if error in self.input_line.text():
                    self.error_line.setText("Error :" + error)
                
                else:
                    if '^' in err_msg:
                        self.error_line.setText("Error :" + err_msg.split('\n')[-4])

                    else:
                        self.error_line.setText("Error :" + err_msg.split('\n')[-3])


    def equation_Clicked(self, equation):
        if self.input_line.text() == self.default_display:
            display = ''
        else:
            display = self.input_line.text()

        # 개선사항 3 23.10.11
        if str(equation) == '(' or str(equation) == ')':
            display = self.paren_error(equation, display)
        else:
            display += equation
        self.input_line.setText(display)


    def backSpace_Clicked(self):
        if self.input_line.text() == self.default_display:
            display = ''
        else:
            display = self.input_line.text()[:-1]
        
        self.input_line.setText(display)

    
    def remove_all(self):
        if self.input_line.text() == self.default_display:
            display = ''
        else:
            display = self.input_line.clear()

        self.input_line.setText(display)


    def calculation(self):
        mathmetical = self.input_line.text().replace('−', '-').replace('×', '*').replace('÷', '/')
        if '²' in mathmetical:
            mathmetical = self.cal_product(mathmetical)
        
        else:
            pass
        
        if '√' in mathmetical:
            mathmetical = self.cal_division(mathmetical)

        else:
            pass

        return mathmetical
    

    def cal_product(self, mathmetical):
        count = mathmetical.count('²')

        for _ in range(count):
            pro_num = ''
            for i in range(mathmetical.index('²')-1, -1, -1):
                if mathmetical[i].isdigit() or mathmetical[i] == '.':
                    pro_num += mathmetical[i]
                else:
                    break

            pro_num = ''.join(reversed(pro_num))
            mathmetical = mathmetical.replace('²', '*' + pro_num, 1)

        return mathmetical


    def cal_division(self, mathmetical):
        count = mathmetical.count('√')

        for _ in range(count):
            div_num = ''
            for i in range(mathmetical.index('√')+1, len(mathmetical)):
                if mathmetical[i].isdigit() or mathmetical[i] == '.':
                    div_num += mathmetical[i]
                else:
                    break

            div_num = ''.join(div_num)
            mathmetical = mathmetical.replace('√' + div_num, div_num + '**(1/2)', 1)
        
        return mathmetical
    

    def paren_error(self, equation, display):
        if str(equation) == '(':
            if len(display) >= 1:
                if display[-1] == '.':
                    self.error_line.setText("소수점 뒤에 괄호를 사용할 수 없습니다.")
                elif display[-1].isdigit() or display[-1] == ')':
                    display = display + '*' + str(equation)
                else:
                    display += str(equation)
            else:
                display += str(equation)
        
        elif str(equation) == ')':
            count = display.count('(')
            if display.count(')') < count:
                if display[-1] == '(' or display[-1] == '.' or display[-1] in self.four_base:
                    self.error_line.setText("폐괄호를 사용할 수 없습니다.")
                else:
                    display += str(equation)
            else:
                self.error_line.setText("더이상 폐괄호를 사용할 수 없습니다.")

        return display



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = MyCalculator()
    myWindows.show()

    sys.exit(app.exec_())
