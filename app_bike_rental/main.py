from app_bike_rental.people import Person
from app_bike_rental.rental_station import Rental_Station


def main():
    rental_station = Rental_Station()
    john = Person("John", "jn", 19)
    rental_station.rent_bike(john, {"Regular": [[john]]})
    print(rental_station.revenue)
    print(rental_station.rentedbikes)
    print(rental_station.rentedbikes[john.id]["Regular"])
    print(rental_station.rentedinventory)
    print(john.rentedbikes)
    print(john.bikeid)

    print("parent, child renters")
    ross = Person("Ross", "rs", 30)
    ben = Person("Ben", "bn", 8)
    rental_station.rent_bike(ross, {"Regular": [[ross]], "Child": [[ben]]})
    print(rental_station.revenue)
    print(rental_station.rentedbikes)
    print(rental_station.rentedinventory)
    print(ross.rentedbikes)
    print(ross.bikeid)
    print(ben.rentedbikes)
    print(ben.bikeid)
    

    print("tandem renters")
    greg = Person("Greg", "gg", 19)
    chris = Person("Chris", "cs", 24)
    rental_station.rent_bike(greg, {"Tandem": [[greg, chris]]})
    print(rental_station.revenue)
    print(rental_station.rentedbikes)
    print(rental_station.rentedinventory)
    print(greg.rentedbikes)
    print(greg.bikeid)
    print(chris.rentedbikes)
    print(chris.bikeid)

    for i in range(60):
        # what if they have the same name
        name = Person(str(i),str(i),20)
        rental_station.rent_bike(name,{"Regular": [[name]], "Child": [[]], "Tandem": [[]]})
        print(rental_station.rentedinventory)

    for i in range(20):
        name = Person(str(i),str(i),20)
        rental_station.rent_bike(name,{"Regular": [[]], "Child": [[name]], "Tandem": [[]]})
        print(rental_station.rentedinventory)

    for i in range(20):
        name = Person(str(i),str(i),20)
        name2 = Person("a"+str(i),str(i),20)
        rental_station.rent_bike(name,{"Regular": [[]], "Child": [[]], "Tandem": [[name, name2]]})
        print(rental_station.rentedinventory)

    print(name.rentedbikes)

main()
