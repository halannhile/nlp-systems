class Shoe: 
    def __init__(self, brand, model, size, color, function): 
        self.brand = brand
        self.model = model
        self.size = size
        self.color = color
        self.function = function 
    
    def __str__(self):
        return f"Shoe: brand {self.brand}, model {self.model}, size {self.size}, color {self.color}, function {self.function}"
    