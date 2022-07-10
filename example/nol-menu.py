from rtadubai import Nol

Flag = False
while Flag is False:
    nol = input("Enter your NOL card number: ")
    try:
        card = Nol.Card(nol)
        Flag = True
    except ValueError:
        print("Invalid NOL card\n")

while True:
    print("\n1. View NOL card Details\n2. View recent NOL Transaction\n3. View all NOL Transaction\n0. Exit")

    choice = int(input("Enter your choice: "))
    print()

    if choice == 1:
        print("Nol Card: \t\t", card.id)
        print("Card Balance: \t\t", card.balance)
        print("Pending Balance: \t", card.pending)
        print("Expiry Date: \t\t", card.expiry)
        print()

    elif choice == 2:
        transaction = card.recent()
        if transaction["Error"] is True:
            print("No transactions found")
        else:
            transaction = transaction["Transaction"]
            print("Date:\t\t" + transaction["Date"])
            print("Time:\t\t" + transaction["Time"])
            print("Type:\t\t" + transaction["Type"])
            print("Amount:\t" + transaction["Amount"] + " AED")
            print()

    elif choice == 3:
        transactions = card.transactions()
        if transactions["Error"] is True:
            print("No transactions found")
        else:
            for transaction in transactions["Transactions"]:
                print("Date:\t\t" + transaction["Date"])
                print("Time:\t\t" + transaction["Time"])
                print("Type:\t\t" + transaction["Type"])
                print("Amount:\t" + transaction["Amount"] + " AED")
                print()
    elif choice == 0:
        break
