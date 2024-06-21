# __init__是必不可少的一个特殊的方法
# 每次创建新实例，都会自动执行


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self):
        print(f"{self.name} is sitting now.")

    def roll(self):
        print(f"{self.name} is rolling.")


puppy1 = Dog("Smith", "3")
puppy1.sit()
puppy1.roll()

puppy2 = Dog("Lucy", "2")
puppy2.sit()
puppy2.roll()


class WorkingDog(Dog):
    def __init__(self, name, age, task):
        super().__init__(name, age)
        self.task = task

    def perform_task(self):
        print(f"{self.name} is performing {self.task}.")


puppy3 = WorkingDog("Alice", 6, "code")
puppy3.perform_task()


class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        long_name = f"{self.year} f{self.make} f{self.model}"
        return long_name.title()

    def read_odometer(self):
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")

    def increment_odometer(self, miles):
        self.odometer_reading += miles


class Battery:
    def __init__(self, battery_size=40):
        self.battery_size = battery_size

    def describe_battery(self):
        print(f"This car has a {self.battery_size}-kWh battery.")


class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()


my_leaf = ElectricCar("nissan", "leaf", 2024)
print(my_leaf.get_descriptive_name())
my_leaf.battery.describe_battery()
