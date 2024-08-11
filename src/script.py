class GoldPriceItem:
    def __init__(self, weight, price_per_gram, service_charge=17, tax=3):
        if weight <= 0 or price_per_gram <= 0 or service_charge < 0 or tax < 0:
            raise ValueError("All inputs must be positive numbers.")
        
        self.weight = weight
        self.price_per_gram = price_per_gram
        self.service_charge = service_charge
        self.tax = tax

    def calculate_tax(self, item_price):
        return item_price * self.tax / 100
        
    def calculate_service_charge(self, item_price):
        return item_price * self.service_charge / 100

    def calculate_price(self):
        base_price = self.weight * self.price_per_gram
        service_charge = self.calculate_service_charge(base_price)
        total_price = base_price + service_charge
        tax = self.calculate_tax(total_price)
        final_price = round(total_price + tax)
        
        return {
            "Base Price": base_price,
            "Service Charge": service_charge,
            "Service Charge Percentage": self.service_charge,
            "Tax": tax,
            "Tax Percentage": self.tax,
            "Final Price": final_price
        }
