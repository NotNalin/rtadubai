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
        try:
            transaction = card.recent()
        except ValueError as e:
            print(e)
            pass
        print("Date:\t\t" + transaction["date"])
        print("Time:\t\t" + transaction["time"])
        print("Type:\t\t" + transaction["type"])
        print("Amount:\t" + transaction["amount"] + " AED")
        print()

    elif choice == 3:
        try:
            transactions = card.transactions()
        except ValueError as e:
            print(e)
            pass
        if len(transactions) == 0:
            print("No Transactions Found")
        else:
            for transaction in transactions:
                print("Date:\t\t" + transaction["date"])
                print("Time:\t\t" + transaction["time"])
                print("Type:\t\t" + transaction["type"])
                print("Amount:\t" + transaction["amount"] + " AED")
                print()
    elif choice == 0:
        break
