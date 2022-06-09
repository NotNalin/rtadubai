from rtadubai import Nol

Flag = False
while Flag is False:
    nol = input('Enter your NOL card number: ').strip().replace(" ", "")
    if len(nol) == 10:
        if nol.isdigit():
            if Nol.isValid(nol) is True:
                Flag = True
                break
    print('Invalid NOL card\n')

while True:
    print('\n1. View NOL card Balance\n2. View recent NOL Transaction\n3. View all NOL Transaction\n0. Exit')

    choice = int(input('Enter your choice: '))
    print()

    if choice == 1:
        print("Card Balance: \t\t", Nol.CardBalance(nol))

    elif choice == 2:
        i = Nol.Recent(nol)
        if i['Error'] is True:
            print("No transactions found")
        else:
            print('Date:\t\t' + i['Date'])
            print('Time:\t\t' + i['Time'])
            print('Type:\t\t' + i['Type'])
            print('Amount:\t' + i['Amount'])
            print()

    elif choice == 3:
        l = Nol.TransactionsRaw(nol)
        if type(l) is not list:
            print("No transactions found")
        else:
            for i in l:
                print('Date:\t\t' + i['Date'])
                print('Time:\t\t' + i['Time'])
                print('Type:\t\t' + i['Type'])
                print('Amount:\t' + i['Amount'] + ' AED')
                print()
    elif choice == 0:
        break
