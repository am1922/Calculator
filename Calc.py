import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from abc import ABC, abstractmethod

class OperationStrategy(ABC):
    @abstractmethod
    def execute(self, a: complex, b: complex) -> complex:
        pass

class AdditionStrategy(OperationStrategy):
    def execute(self, a: complex, b: complex) -> complex:
        return a + b

class MultiplicationStrategy(OperationStrategy):
    def execute(self, a: complex, b: complex) -> complex:
        return a * b

class DivisionStrategy(OperationStrategy):
    def execute(self, a: complex, b: complex) -> complex:
        if b == 0:
            raise ValueError("Деление на ноль невозможно.")
        return a / b


class Calculator:
    def __init__(self, strategy: OperationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: OperationStrategy):
        self._strategy = strategy

    def calculate(self, a: complex, b: complex) -> complex:
        result = self._strategy.execute(a, b)
        logging.info(f"Operation: {self._strategy.__class__.__name__}, Result: {result}")
        return result


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.strategy_combobox = QComboBox()
        self.strategy_combobox.addItems(["Сложение", "Умножение", "Деление"])

        self.number1_input = QLineEdit(self)
        self.number2_input = QLineEdit(self)
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)

        self.calculate_button = QPushButton("Вычислить", self)
        self.calculate_button.clicked.connect(self.calculate)

        self.init_ui()
        self.setup_logging()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Выберите операцию:"), alignment=Qt.AlignTop)
        layout.addWidget(self.strategy_combobox, alignment=Qt.AlignTop)

        layout.addWidget(QLabel("Введите первое комплексное число:"), alignment=Qt.AlignTop)
        layout.addWidget(self.number1_input, alignment=Qt.AlignTop)

        layout.addWidget(QLabel("Введите второе комплексное число:"), alignment=Qt.AlignTop)
        layout.addWidget(self.number2_input, alignment=Qt.AlignTop)

        layout.addWidget(self.calculate_button, alignment=Qt.AlignTop)

        layout.addWidget(QLabel("Логи:"), alignment=Qt.AlignTop)
        layout.addWidget(self.log_output, alignment=Qt.AlignTop)

    def calculate(self):
        try:
            complex_number1 = complex(self.number1_input.text().replace("j", "J"))
            complex_number2 = complex(self.number2_input.text().replace("j", "J"))

            selected_strategy = self.get_selected_strategy()
            calculator = Calculator(selected_strategy)
            result = calculator.calculate(complex_number1, complex_number2)
          
            self.number1_input.clear()
            self.number2_input.clear()

            self.log_output.append(f"Результат: {result}")

        except ValueError as e:
            self.handle_error(e, "Ошибка при выполнении вычислений")
        except ZeroDivisionError as e:
            self.handle_error(e, "Деление на ноль невозможно.")

    def handle_error(self, error, message):
        logging.error(f"Error during calculation: {str(error)}")
        self.log_output.append(f"Ошибка: {str(error)}")
        QMessageBox.critical(self, "Ошибка", f"{message}: {str(error)}")

    def get_selected_strategy(self) -> OperationStrategy:
        strategy_name = self.strategy_combobox.currentText()
        strategy_mapping = {
            "Сложение": AdditionStrategy(),
            "Умножение": MultiplicationStrategy(),
            "Деление": DivisionStrategy()
        }
        return strategy_mapping.get(strategy_name, AdditionStrategy())

    def setup_logging(self):
        logging.basicConfig(filename='calculator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        if not any(isinstance(handler, QTextEditHandler) for handler in logging.getLogger().handlers):
            handler = QTextEditHandler(self.log_output)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(handler)


class QTextEditHandler(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator_app = CalculatorApp()
    calculator_app.show()
    sys.exit(app.exec_())
