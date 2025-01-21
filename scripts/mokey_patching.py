class Car():
    def start(self, ceva):
        print(f"Start the car {ceva}")


car = Car()

car.start("bam")

def new_starting(self):
    print("Start the car using a new method")

Car.start = new_starting

car.start()


