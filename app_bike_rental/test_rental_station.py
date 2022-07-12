from unittest import TestCase

from app_bike_rental.people import Person, NotAdultException
from app_bike_rental.rental_station import Rental_Station, AdultException, TandemException


class Test_Rental_Station(TestCase):

    def setUp(self):
        self.rental_station = Rental_Station()

    def test_regular_rental(self):
        john = Person("John", "jn", 19)
        self.rental_station.rent_bike(john, {"Regular": [[john]]})

        self.assertEqual(self.rental_station.revenue, 10)
        self.assertTrue(john.bikeid in self.rental_station.rentedbikes[john.id]["Regular"])
        self.assertEqual(self.rental_station.rentedinventory["Regular"], 59)


    def test_child_rental(self):
        ross = Person("Ross", "rs", 30)
        ben = Person("Ben", "bn", 8)
        self.rental_station.rent_bike(ross, {"Regular": [[ross]], "Child": [[ben]]})

        self.assertEqual(self.rental_station.revenue, 18)
        self.assertTrue(ross.bikeid in self.rental_station.rentedbikes[ross.id]["Regular"])
        self.assertTrue(ben.bikeid in self.rental_station.rentedbikes[ross.id]["Child"])
        self.assertEqual(self.rental_station.rentedinventory["Regular"], 59)
        self.assertEqual(self.rental_station.rentedinventory["Child"], 19)

    def test_tandem_rental(self):
        greg = Person("Greg", "gg", 19)
        chris = Person("Chris", "cs", 24)
        self.rental_station.rent_bike(greg, {"Tandem": [[greg, chris]]})

        self.assertEqual(self.rental_station.revenue, 17)
        self.assertTrue(greg.bikeid in self.rental_station.rentedbikes[greg.id]["Tandem"])
        self.assertEqual(self.rental_station.rentedinventory["Tandem"], 19)
        self.assertEqual(chris.bikeid, greg.bikeid)

    def test_run_out_regular(self):
        for i in range(60):
            name = Person(str(i), str(i), 20)
            self.rental_station.rent_bike(name, {"Regular": [[name]]})

        john = Person("John", "jn", 19)
        self.rental_station.rent_bike(john, {"Regular": [[john]]})

        self.assertEqual(self.rental_station.revenue, 600)
        self.assertEqual(self.rental_station.rentedinventory["Regular"], 0)
        self.assertTrue(john.bikeid is None)
        self.assertEqual(self.rental_station.rentedinventory["Child"], 20)
        self.assertEqual(self.rental_station.rentedinventory["Tandem"], 20)

    def test_run_out_child(self):
        for i in range(20):
            name = Person(str(i), str(i), 20)
            name2 = Person("C"+str(i), "C"+str(i), 10)
            self.rental_station.rent_bike(name, {"Child": [[name2]]})

        ross = Person("Ross", "rs", 30)
        ben = Person("Ben", "bn", 8)
        self.rental_station.rent_bike(ross, {"Child": [[ben]]})

        self.assertEqual(self.rental_station.revenue, 160)
        self.assertEqual(self.rental_station.rentedinventory["Child"], 0)
        self.assertTrue(ben.bikeid is None)
        self.assertEqual(self.rental_station.rentedinventory["Regular"], 60)
        self.assertEqual(self.rental_station.rentedinventory["Tandem"], 20)

    def test_run_out_tandem(self):
        for i in range(20):
            name = Person(str(i), str(i), 20)
            name2 = Person("a" + str(i), str(i), 20)
            self.rental_station.rent_bike(name, {"Tandem": [[name, name2]]})

        greg = Person("Greg", "gg", 19)
        chris = Person("Chris", "cs", 24)
        self.rental_station.rent_bike(greg, {"Tandem": [[greg, chris]]})

        self.assertEqual(self.rental_station.revenue, 340)
        self.assertEqual(self.rental_station.rentedinventory["Tandem"], 0)
        self.assertTrue(greg.bikeid is None)
        self.assertTrue(chris.bikeid is None)
        self.assertEqual(self.rental_station.rentedinventory["Regular"], 60)
        self.assertEqual(self.rental_station.rentedinventory["Child"], 20)

    def test_child_payment(self):
        ben = Person("Ben", "bn", 8)
        with self.assertRaises(NotAdultException) as ec:
            self.rental_station.rent_bike(ben, {"Child": [[ben]]})

    def test_adult_child_bike(self):
        john = Person("John", "jn", 19)
        with self.assertRaises(AdultException) as ec:
            self.rental_station.rent_bike(john, {"Child": [[john]]})

    def test_one_person_tandem(self):
        greg = Person("Greg", "gg", 19)
        with self.assertRaises(TandemException) as ec:
            self.rental_station.rent_bike(greg, {"Tandem": [[greg]]})

    def test_input(self):
        john = Person("John", "jn", 19)
        ben = Person("Ben", "bn", 8)
        greg = Person("Greg", "gg", 19)
        chris = Person("Chris", "cs", 24)
        self.rental_station.rent_bike(john, {"Rgular": [[john]], "Chld": [[ben]], "Tandm": [[greg, chris]]})

        self.assertEqual(self.rental_station.revenue, 0)
        self.assertTrue(john.bikeid is None)
        self.assertTrue(ben.bikeid is None)
        self.assertTrue(greg.bikeid is None)
        self.assertTrue(chris.bikeid is None)
        self.assertEqual(self.rental_station.rentedbikes[john.id]["Regular"], [])
        self.assertEqual(self.rental_station.rentedbikes[john.id]["Child"], [])
        self.assertEqual(self.rental_station.rentedbikes[john.id]["Tandem"], [])

        self.assertEqual(self.rental_station.rentedinventory["Regular"], 60)
        self.assertEqual(self.rental_station.rentedinventory["Child"], 20)
        self.assertEqual(self.rental_station.rentedinventory["Tandem"], 20)

    def test_two_bikes(self):
        john = Person("John", "jn", 19)
        self.rental_station.rent_bike(john, {"Regular": [[john], [john]]})
        self.assertEqual(self.rental_station.revenue, 10)
        self.assertTrue(john.bikeid in self.rental_station.rentedbikes[john.id]["Regular"])
        self.assertEqual(len(self.rental_station.rentedbikes[john.id]["Regular"]), 1)
        self.assertEqual(self.rental_station.rentedinventory["Regular"], 59)
