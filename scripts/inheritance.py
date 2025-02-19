class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self._fullname = self.make + self.model
        self.__started = False

    def __macaroane(self):
        print(f"Macaroane {self.make}")


class Car(Vehicle):
    def __init__(self, make, model, year, wheels):
        super().__init__(make, model, year)
        self.wheels = wheels
        
    def start_engine(self):
        if not self._Vehicle__started:
            print("Start the engine...")
            self._Vehicle__started = True
        else:
            print("Engine already started")

    def stop_engine(self):
        if self._Vehicle__started:
            print("Stop the engine")
            self._Vehicle__started = False
        else:
            print("Engine already stopped")

    def driving(self):
        print(self._fullname)
        print(f"Driving this excelent {self.make} {self.model} Car from {self.year}")

tesla = Car("Tesla", "Model 3", "2022", "4")
bicicleta = Vehicle("Pegas", "312", "2003")
print(tesla._Vehicle__macaroane())

print(dir(Car))
print(Car.__dict__)


# bicicleta.
# tesla.macaroane()
