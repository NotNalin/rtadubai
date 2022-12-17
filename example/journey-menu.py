from rtadubai import Shail
import json

startname = input("Enter start point: ")
stops = Shail.stopnames(startname)

if len(stops) == 0:
    print("No stops found")
    exit()

for index, stop in enumerate(stops):
    print(f"{index + 1}. {stop}")

choice = int(input("Enter stop number : "))
start = Shail.Stop(stops[choice - 1])

endname = input("Enter end point: ")
stops = Shail.stopnames(endname)

if len(stops) == 0:
    print("No stops found")
    exit()

for index, stop in enumerate(stops):
    print(f"{index + 1}. {stop}")

choice = int(input("Enter stop number : "))
end = Shail.Stop(stops[choice - 1])

journey = Shail.journey_planner(start, end)
print(json.dumps(journey, indent=4))