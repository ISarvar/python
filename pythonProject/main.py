from tkinter import *


# Класс для калькулятора
class LoanCalculator:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x300")
        self.root.title("Кредитный калькулятор")
        self.root.config(bg='#a39ea0')

        Label(self.root, text="Годовая ставка, %", font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=10, y=10)
        Label(self.root, text="Срок, лет", font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=10, y=50)
        Label(self.root, text="Сумма кредита", font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=10, y=90)
        Label(self.root, text="Ежемесячный платёж:", font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=10, y=150)
        Label(self.root, text="Общая сумма выплаты:", font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=10, y=190)

        self.annualinterestVar = StringVar()
        Entry(self.root, textvariable=self.annualinterestVar, font=('Arial', 15, 'bold')).place(x=220, y=10)

        self.numberofyearsVar = StringVar()
        Entry(self.root, textvariable=self.numberofyearsVar, font=('Arial', 15, 'bold')).place(x=220, y=50)

        self.loanamountVar = StringVar()
        Entry(self.root, textvariable=self.loanamountVar, font=('Arial', 15, 'bold')).place(x=220, y=90)

        self.monthlypaymentVar = StringVar()
        Label(self.root, textvariable=self.monthlypaymentVar, font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=220,
                                                                                                              y=150)

        self.totalpaymentVar = StringVar()
        Label(self.root, textvariable=self.totalpaymentVar, font=('Arial', 15, 'bold'), bg='#a39ea0').place(x=220,
                                                                                                            y=190)

        Button(self.root, text="Рассчитать", font=('Arial', 15, 'bold'), command=self.calculateloan).place(x=180, y=240)

        self.root.mainloop()

    def calculateloan(self):
        try:
            loan_amount = float(self.loanamountVar.get())
            annual_interest = float(self.annualinterestVar.get())
            number_of_years = int(self.numberofyearsVar.get())

            monthly_payment = self.getmonthlyPayment(loan_amount, annual_interest / 1200, number_of_years)
            self.monthlypaymentVar.set(f"{monthly_payment:.2f}")

            total_payment = monthly_payment * 12 * number_of_years
            self.totalpaymentVar.set(f"{total_payment:.2f}")
        except ValueError:
            self.monthlypaymentVar.set("Ошибка ввода")
            self.totalpaymentVar.set("Ошибка ввода")

    def getmonthlyPayment(self, loan_amount, monthly_interest_rate, number_of_years):
        monthly_payment = loan_amount * monthly_interest_rate / (
                    1 - (1 + monthly_interest_rate) ** -(number_of_years * 12))
        return monthly_payment


# Класс калькулятора для запуска программы
LoanCalculator()
