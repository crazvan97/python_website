class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.__started = False

    def __macaroane(self):
        print(f"Macaroane {self.make}")

    


class Car(Vehicle):
    def __init__(self, make, model, year, wheels):
        super().__init__(make, model, year)
        self.wheels = wheels
        
    def start_engine(self):
        if not self.__started:
            print("Start the engine...")
            self.__started = True
        else:
            print("Engine already started")

    def stop_engine(self):
        if self.__started:
            print("Stop the engine")
            self.__started = False
        else:
            print("Engine already stopped")

    def driving(self):
        print(f"Driving this excelent {self.make} {self.model} Car from {self.year}")

tesla = Car("Tesla", "Model 3", "20222", "4")
bicicleta = Vehicle("Pegas", "312", "2003")
tesla.driving()
tesla.start_engine()
tesla.stop_engine()
tesla.stop_engine()
tesla.start_engine()
tesla.start_engine()

# bicicleta.
# tesla.macaroane()
