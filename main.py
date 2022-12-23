import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from main_window import Ui_MainWindow
import requests
from bs4 import BeautifulSoup
import webbrowser


class CurrencyConverter(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrencyConverter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Currency converter')
        self.setWindowIcon(QIcon('icon.png'))
        self.ui.Input_1.setPlaceholderText('RUB')
        self.ui.Input_amount.setPlaceholderText('100')
        self.ui.Input_2.setPlaceholderText('USD')
        self.ui.Input_amount_2.setPlaceholderText('')
        self.ui.Convert_button.clicked.connect(self.converter)
        self.ui.HTMLlink_button.clicked.connect(lambda: webbrowser.open('https://www.ups.com/worldshiphelp/WSA/RUS/AppHelp/mergedProjects/CORE/Codes/Country_Territory_and_Currency_Codes.htm'))

    def converter(self):
        def get_html(url):
            HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/102.0.5005.61 Safari/537.36',
                'Accept': '*/*'
            }
            try:
                r = requests.get(url, headers=HEADERS, timeout=5)
                r.encoding = 'utf-8'
                return r
            except Exception:
                output_exception = 'WRONG'
                self.ui.label_4.setText(output_exception)
                return None

        def get_currency(html):
            soup = BeautifulSoup(html, 'html.parser')
            full_text_currency = soup.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod')
            currency = full_text_currency.get_text(strip=False)
            text_part_of_currency = full_text_currency.find('span', class_='faded-digits').get_text(strip=False)
            currency_new = currency.replace(text_part_of_currency, '')
            ration = soup.find('div', class_='unit-rates___StyledDiv-sc-1dk593y-0 dEqdnx').find('p').get_text(strip=False)
            return [currency_new, ration]

        input_currency = self.ui.Input_1.text()
        output_currency = self.ui.Input_2.text()
        input_amount = int(self.ui.Input_amount.text())

        url = f'https://www.xe.com/currencyconverter/convert/?Amount' \
              f'={input_amount}&From={input_currency}&To={output_currency}'
        try:
            html = get_html(url)
            try:
                currency_parse = get_currency(html.text)
                output_amount, output_ration = currency_parse[0], currency_parse[1]
            except:
                output_amount, output_ration = 'Error', ''
        except:
            output_amount, output_ration = 'Error', ''
        self.ui.Input_amount_2.setText(str(output_amount))
        self.ui.Output_2.setText(str(output_ration))


app = QtWidgets.QApplication([])
application = CurrencyConverter()
application.show()

sys.exit(app.exec())

