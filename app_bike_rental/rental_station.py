"""
inventory
payments/costs
    - how much each bike costs
    - people need to pay
when people rent out the bikes, keep track of who has what bike
when people return the bike
keep track of time -- notify people when their time is almost up
no cool down period, but people cannot extend their bike time (need to bring it back, and resign it out)

"""
from collections import defaultdict

from test_applications.oop.app_bike_rental.bikes import Regular, Child, Tandem

class AdultException(Exception):
    pass

class TandemException(Exception):
    pass

class Rental_Station:
    def __init__(self):
        self.totalinventory = 100
        self.percentsingle = .6
        self.percentchild = .2
        self.percenttandem = .2
        self.pricing = {"Regular": 10, "Child": 8, "Tandem": 17}
        self.rentedbikes = defaultdict(lambda: defaultdict(lambda: []))
        self.rentedinventory = {"Regular": int(self.totalinventory * self.percentsingle),
                                "Child": int(self.totalinventory * self.percentchild),
                                "Tandem": int(self.totalinventory * self.percenttandem)}
        self.revenue = 0


    def rent_bike(self, renter, want_to_rent):
        #want_to_rent = {type: [[rider1], [rider2], rider3], tandem: [[person1, person2], [],}
        for key in want_to_rent:
            if key not in self.rentedinventory:
                print("Sorry that is not an acceptable bike type")
                continue
            for number in range(len(want_to_rent[key])):
                self._make_bike(renter, want_to_rent[key][number], key)

    def _make_bike(self, renter, rider, bike_type):
        if self.rentedinventory[bike_type] <= 0:
            print(f"Sorry there are not enough {bike_type.lower()} bikes.")
            return

        for person in rider:
            if person.bikeid is not None:
                print("Sorry this person is already riding a bike")
                return

        self.rentedinventory[bike_type] -= 1

        cost = self.pricing[bike_type]
        if bike_type == "Regular":
            self._handle_regular_bike(renter, rider[0], cost)
        if bike_type == "Child":
            self._handle_child_bike(renter, rider[0], cost)
        if bike_type == "Tandem":
            self._handle_tandem_bike(renter, rider, cost)
        self.revenue += cost

    def _handle_regular_bike(self, renter, rider, cost):
        bike = Regular(renter, rider)
        rider.get_bike(bike.id)
        self.rentedbikes[renter.id]["Regular"].append(rider.bikeid)
        renter.make_payment(cost, bike.id)


    def _handle_child_bike(self, renter, rider, cost):
        if rider[0].age > 12:
            raise AdultException

        bike = Child(renter, rider)
        rider.get_bike(bike.id)
        self.rentedbikes[renter.id]["Child"].append(rider.bikeid)
        renter.make_payment(cost, bike.id)


    def _handle_tandem_bike(self, renter, rider, cost):
        if len(rider) != 2:
            print("Sorry tandem bikes require two people")
            raise TandemException

        bike = Tandem(renter, rider)
        rider[0].get_bike(bike.id)
        rider[1].get_bike(bike.id)
        self.rentedbikes[renter.id]["Tandem"].append(rider[0].bikeid)
        # self.rentedbikes[renter.id]["Tandem"].append(rider[1].bikeid)
        renter.make_payment(cost, bike.id)







