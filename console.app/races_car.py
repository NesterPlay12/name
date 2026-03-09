import random


class Car:
    def __init__(self, brand, model, year, price, color="Белый", doors=4, horsepower=250):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.color = color
        self.doors = doors
        self.mileage = 0
        self.engine_on = False
        self.horsepower = horsepower
        self.wins = 0

    def info(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.price}$ [{self.color}, {self.doors} двери, {self.horsepower} л.с., {self.wins} побед]"


class SportCar(Car):
    def __init__(self, brand, model, year, price, color="Красный", doors=2, horsepower=400):
        super().__init__(brand, model, year, price, color, doors, horsepower)
        self.nitro = True


class Garage:
    def __init__(self, owner):
        self.owner = owner
        self.cars = []
        self.money = 10000

    def add_car(self, car):
        self.cars.append(car)
        print(f"✅ {car.brand} {car.model} добавлена в гараж!")

    def remove_car(self, index):
        if 0 <= index < len(self.cars):
            car = self.cars.pop(index)
            self.money += car.price // 2
            print(f"💰 {car.brand} {car.model} продана за {car.price // 2}$!")

    def show_garage(self):
        print(f"\n🚗 ГАРАЖ {self.owner} | Деньги: {self.money}$")
        if not self.cars:
            print("Пусто...")
        else:
            for i, car in enumerate(self.cars):
                print(f"{i + 1}. {car.info()}")

    def race_participation(self, car_index, race):
        if car_index < 0 or car_index >= len(self.cars):
            print("❌ Нет такой машины!")
            return

        my_car = self.cars[car_index]

        if not race.can_participate(my_car):
            print(
                f"❌ {my_car.brand} {my_car.model} не допущена до гонки! Мощность {my_car.horsepower} л.с., нужно минимум {race.min_horsepower} л.с.")
            return

        print("\n📋 Участники из вашего гаража:")
        for i, car in enumerate(self.cars):
            status = "✅ допущена" if race.can_participate(car) else "❌ не допущена"
            print(f"{i + 1}. {car.brand} {car.model} ({car.horsepower} л.с.) - {status}")

        # Исправлено: передаем только participants
        participants = [car for car in self.cars if race.can_participate(car)]
        winner = race.race(participants)

        if winner is None:
            print("😕 Гонка не состоялась (нет участников).")
            return

        if winner == my_car:
            self.money += race.prize
            my_car.wins += 1
            my_car.horsepower += 5
            print(f"🏆 ПОБЕДА! {my_car.brand} {my_car.model} выиграла гонку!")
            print(f"💰 Получено {race.prize}$ | Теперь у вас {self.money}$")
            print(f"⚡ Мощность увеличена на 5 л.с. (теперь {my_car.horsepower} л.с.)")
        else:
            print(f"😢 Ваша машина ({my_car.brand} {my_car.model}) проиграла.")
            print(f"Победитель: {winner.brand} {winner.model} ({winner.horsepower} л.с., побед: {winner.wins})")

    def edit_car(self, index):
        if 0 <= index < len(self.cars):
            car = self.cars[index]
            print(f"\n✏️ РЕДАКТИРУЕМ: {car.info()}")
            print("Что меняем?")
            print("1. Цвет")
            print("2. Цену")
            print("3. Количество дверей")
            print("0. Отмена")

            choice = input("Выбор: ")

            if choice == "1":
                new_color = input("Новый цвет: ")
                car.color = new_color
                print("✅ Цвет изменён!")

            elif choice == "2":
                try:
                    new_price = int(input("Новая цена: "))
                    car.price = new_price
                    print("✅ Цена изменена!")
                except:
                    print("❌ Ошибка! Цена должна быть числом.")

            elif choice == "3":
                try:
                    new_doors = int(input("Новое количество дверей (2 или 4): "))
                    if new_doors in [2, 4]:
                        car.doors = new_doors
                        print("✅ Двери изменены!")
                    else:
                        print("❌ Только 2 или 4!")
                except:
                    print("❌ Ошибка! Введи число.")

            elif choice == "0":
                print("Отмена")
            else:
                print("❌ Неверный выбор!")
        else:
            print("❌ Нет такой машины!")


class AutoShop:
    def __init__(self):
        self.cars_for_sale = [
            Car("Toyota", "Camry", 2020, 8000, "Черный", 4, 350),
            Car("Lada", "Vesta", 2022, 4500, "Красный", 4, 280),
            Car("BMW", "X5", 2019, 10000, "Синий", 4, 390),
            SportCar("Porsche", "911", 2023, 15000, "Желтый", 2, 450),
            Car("Honda", "Civic", 2021, 6500, "Серебро", 4, 330),
        ]

    def show_cars(self):
        print("\n🏢 АВТОСАЛОН:")
        for i, car in enumerate(self.cars_for_sale):
            print(f"{i + 1}. {car.info()}")

    def buy_car(self, index, garage):
        if 0 <= index < len(self.cars_for_sale):
            car = self.cars_for_sale[index]
            if garage.money >= car.price:
                garage.money -= car.price
                garage.add_car(car)
                self.cars_for_sale.pop(index)
                print("🎉 Покупка успешна!")
            else:
                print("❌ Не хватает денег!")


class Race:
    def __init__(self, name, prize, min_horsepower):
        self.name = name
        self.prize = prize
        self.min_horsepower = min_horsepower

    def can_participate(self, car):
        return car.horsepower >= self.min_horsepower

    def race(self, participants):
        if not participants:
            return None

        lottery = []
        for car in participants:
            lottery.extend([car] * car.horsepower)

        winner = random.choice(lottery)
        return winner


RACES = [
    Race("Легкая гонка", 1000, 300),
    Race("Средняя гонка", 2500, 350),
    Race("Сложная гонка", 5000, 400),
    Race("Экстремальная гонка", 8000, 450),
]


def main():
    print("🏁 АВТОСАЛОН 'МЕГА-ДРАЙВ' 🏁")
    name = input("Имя владельца: ")

    garage = Garage(name)
    shop = AutoShop()

    while True:
        print("\n" + "=" * 30)
        print("1. 🚗 Мой гараж")
        print("2. 🏢 Автосалон")
        print("3. ➕ Создать свою машину")
        print("4. 💰 Продать машину")
        print("5. ✏️ Редактировать машину")
        print("6. 🏁 Гонки")
        print("7. 📊 Рейтинг машин")
        print("8. 🚪 Выход")

        choice = input("Выбор: ")

        if choice == "1":
            garage.show_garage()

        elif choice == "2":
            shop.show_cars()
            try:
                num = int(input("Номер машины для покупки (0 - назад): ")) - 1
                if num >= 0:
                    shop.buy_car(num, garage)
            except:
                print("Ошибка ввода!")

        elif choice == "3":
            print("\n🛠️ СОЗДАНИЕ АВТОМОБИЛЯ")
            try:
                brand = input("Марка: ")
                model = input("Модель: ")
                year = int(input("Год: "))
                price = int(input("Цена: "))
                color = input("Цвет (оставьте пустым для стандартного): ")
                if not color:
                    color = "Белый"

                car_type = input("Спортивный? (да/нет): ")
                doors = int(input("Сколько дверей? (2/4): "))
                horsepower = int(input("Сколько лошадиных сил? (минимум 150): "))

                if horsepower < 150:
                    print("Минимум 150, устанавливаю 150.")
                    horsepower = 150

                if doors not in [2, 4]:
                    print("Так не бывает. Ставлю 4.")
                    doors = 4

                if car_type.lower() == "да":
                    new_car = SportCar(brand, model, year, price, color, doors, horsepower)
                else:
                    new_car = Car(brand, model, year, price, color, doors, horsepower)

                if garage.money >= price:
                    garage.money -= price
                    garage.add_car(new_car)
                    print("✨ Машина создана и добавлена в гараж!")
                else:
                    print(f"❌ Денег не хватает на создание! Нужно {price}$, у вас {garage.money}$")
            except ValueError:
                print("❌ Ошибка ввода! Проверьте правильность введенных данных.")

        elif choice == "4":
            garage.show_garage()
            if garage.cars:
                try:
                    num = int(input("Номер машины для продажи: ")) - 1
                    garage.remove_car(num)
                except:
                    print("Ошибка!")

        elif choice == "5":
            garage.show_garage()
            if garage.cars:
                try:
                    num = int(input("Номер машины для редактирования: ")) - 1
                    garage.edit_car(num)
                except:
                    print("Ошибка!")

        elif choice == "6":
            if not garage.cars:
                print("У вас нет машин! Сначала купите или создайте.")
                continue

            print("\n🏁 Доступные гонки:")
            for i, race in enumerate(RACES):
                print(f"{i + 1}. {race.name} | Приз: {race.prize}$ | Мин. мощность: {race.min_horsepower} л.с.")

            try:
                race_num = int(input("Выберите номер гонки (0-назад): ")) - 1
                if race_num < 0 or race_num >= len(RACES):
                    continue

                race = RACES[race_num]
                garage.show_garage()
                car_num = int(input("Номер вашей машины для участия: ")) - 1

                if car_num < 0 or car_num >= len(garage.cars):
                    print("Неверный номер машины.")
                    continue

                garage.race_participation(car_num, race)

            except ValueError:
                print("Ошибка ввода!")

        elif choice == "7":
            if not garage.cars:
                print("В гараже нет машин, рейтинг пуст.")
                continue

            sorted_cars = sorted(garage.cars, key=lambda c: c.wins, reverse=True)

            print("\n📊 Рейтинг машин по победам:")
            medals = ["🥇", "🥈", "🥉"]
            for i, car in enumerate(sorted_cars):
                place = i + 1
                medal = medals[i] if i < 3 else f"{place}."
                print(f"{medal} {car.brand} {car.model} - {car.wins} побед ({car.horsepower} л.с.)")

        elif choice == "8":
            print("👋 До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()