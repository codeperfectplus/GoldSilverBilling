class GoldCalculator:
    """
    A class to represent an item for which the gold price is calculated.

    Attributes:
        weight (float): Weight of the gold item in grams.
        price_per_gram (float): Price of gold per gram.
        service_charge (float): Service charge percentage applied to the base price (default is 17%).
        tax (float): Tax percentage applied to the total price (default is 3%).

    Methods:
        calculate_tax(item_price): Calculates the tax based on the given item price.
        calculate_service_charge(item_price): Calculates the service charge based on the given item price.
        calculate_price(): Calculates the total price including base price, service charge, and tax.
    """

    def __init__(self, weight, price_per_gram, service_charge=17, tax=3):
        """
        Initializes a GoldPriceItem instance.

        Args:
            weight (float): Weight of the gold item in grams.
            price_per_gram (float): Price of gold per gram.
            service_charge (float, optional): Service charge percentage. Defaults to 17.
            tax (float, optional): Tax percentage. Defaults to 3.

        Raises:
            ValueError: If any of the input values are not positive numbers.
        """
        if weight <= 0 or price_per_gram <= 0 or service_charge < 0 or tax < 0:
            raise ValueError("All inputs must be positive numbers.")
        
        self.weight = weight
        self.price_per_gram = price_per_gram
        self.service_charge = service_charge
        self.tax = tax

    def calculate_tax(self, item_price):
        """
        Calculates the tax based on the given item price.

        Args:
            item_price (float): The price of the item before tax.

        Returns:
            float: The tax amount.
        """
        return round(item_price * self.tax / 100, 2)
        
    def calculate_service_charge(self, item_price):
        """
        Calculates the service charge based on the given item price.

        Args:
            item_price (float): The price of the item before service charge.

        Returns:
            float: The service charge amount.
        """
        return round(item_price * self.service_charge / 100, 2)

    def calculate_price(self):
        """
        Calculates the final price of the gold item, including base price, service charge, and tax.

        Returns:
            dict: A dictionary with the base price, service charge, service charge percentage,
                  tax, tax percentage, and final price.
        """
        base_price = round(self.weight * self.price_per_gram, 2)
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

