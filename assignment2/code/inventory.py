# I did this in Python since I'm most comfortable with it. 

class Shoe:
    def __init__(self, brand, model, size, color, function):
        self.brand = brand
        self.model = model
        self.size = size
        self.color = color
        self.function = function

    def __str__(self):
        return f"Shoe: brand {self.brand}, model {self.model}, size {self.size}, color {self.color}, function {self.function}"

class Inventory:
    def __init__(self):
        self.inventory = []

    def add_shoe(self, shoe):
        self.inventory.append(shoe)

    def sell_shoe(self, shoe):
        print(f"Beging the process of selling {shoe.__str__()}")
        if shoe in self.inventory:
            self.inventory.remove(shoe)
            print(f"Sold: {shoe}")
        else:
            print("Shoe not found in inventory, cannot sell.")

    def list_inventory(self):
        print("Current Inventory:")
        for shoe in self.inventory:
            print(shoe)

    def search(self, brand=None, model=None, size=None, color=None, function=None):
        result = []
        for shoe in self.inventory:
            if (brand is None or shoe.brand == brand) and \
               (model is None or shoe.model == model) and \
               (size is None or shoe.size == size) and \
               (color is None or shoe.color == color) and \
               (function is None or shoe.function == function):
                result.append(shoe)
        return result

# Class Main to demonstrate functionality
class Main:
    def __init__(self):
        self.inventory = Inventory()

    def run(self):
        # Adding some shoes to the inventory
        self.inventory.add_shoe(Shoe("brand1", "model1", "size1", "color1", "function1"))
        self.inventory.add_shoe(Shoe("brand2", "model2", "size2", "color2", "function2"))
        self.inventory.add_shoe(Shoe("brand3", "model3", "size3", "color3", "function3"))

        # Listing the current inventory
        self.inventory.list_inventory()

        # Searching for shoes
        results = self.inventory.search(brand="brand1")
        print("\nSearch results for brand1:")
        for shoe in results:
            print(shoe)

        # Selling a shoe
        self.inventory.sell_shoe(Shoe("brand2", "model2", "size2", "color2", "function2"))

        # Listing the updated inventory
        self.inventory.list_inventory()

if __name__ == "__main__":
    main = Main()
    main.run()

