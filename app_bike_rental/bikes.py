class Bike:

    def __init__(self, renter, id):
        self.renter = renter
        self.id = id


class Regular(Bike):
    def __init__(self, renter, rider):
        super().__init__(renter, "R"+rider.id)
        self.rider = rider


class Child(Bike):
    def __init__(self, renter, child):
        super().__init__(renter, "C" + child.id)
        self.rider = child


class Tandem(Bike):
    def __init__(self, renter, riders):
        super().__init__(renter, "T" + riders[0].id + "T" + riders[1].id)
        self.rider = riders