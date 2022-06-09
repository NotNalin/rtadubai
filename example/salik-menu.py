from rtadubai import Salik

plate = input("Enter your vehicle's plate number: ")
number = input('Enter your mobile number: ')


expiry = Salik.Expiry(plate)
balance = Salik.Balance_Plate(plate, number)


print("Your vehicle's registration expires on:", expiry)
print('Your Salik balance is:', balance, 'AED')
