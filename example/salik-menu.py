from rtadubai import Salik

print("""
1. Dubai
2. Abu Dhabi
3. Sharjah
4. Ajman
5. Umm Al Quwain
6. Ras Al Khaimah
7. Fujairah
""")

area = input("Enter your numer plate's registration area: ")

try:
    area = int(area)
    plates = Salik.plates(area)
except ValueError:
    print("Invalid Area Code")
    exit()

code = input("Enter your numer plate's registration code: ")
if code.upper() not in plates:
    print("Invalid Registration Code")
    exit()

number = input("Enter your numer plate's registration number: ")
mobile = input("Enter your mobile number: ")
print()

try:
    balance = Salik.balance(code, number, mobile, area=area)
    if area == 1:
        expiry = Salik.expiry(code + number)
        print("Your vehicle's registration expires on:", expiry)
    print("Your Salik balance is:", balance, "AED")
except ValueError as e:
    print(e)
