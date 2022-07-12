class NotAdultException(Exception):
    pass




class Person:
    def __init__(self, name, id, age):
        self.name = name
        self.id = id
        self.age = age
        self.rentedbikes = []
        self.bikeid = None

    def make_payment(self, cost, bike_id):
        if self.age < 12:
            print("Unsuccessful Payment")
            raise NotAdultException
        print("Successful Payment")
        self.rentedbikes.append(bike_id)
        return cost

    def get_bike(self, bike_id):
        self.bikeid = bike_id