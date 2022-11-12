from rtadubai import Shail

stopname = input("Enter stop name to check departures: ")
stops = Shail.stopnames(stopname)

if len(stops) == 0:
    print("No stops found")
    exit()

for index, stop in enumerate(stops):
    print(f"{index + 1}. {stop}")

choice = int(input("Enter stop number : "))
stop = Shail.Stop(stops[choice - 1])

departures = Shail.departures(stop)
if len(departures) == 0:
    print("\nNo departures found")
    exit()

print(f"\n{len(departures)} departures found\n")

for departure in departures:
    print("Mode:\t\t", departure["mode"])
    print("Type:\t\t", departure["type"])
    print("Direction:\t", departure["direction"])
    print("Scheuled Time:\t", departure["scheduled_time"])
    print("Estimated Time:\t", departure["estimated_time"])
    print("Status:\t\t", departure["status"])
    print()
