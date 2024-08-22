from sanatio import Sanatio

sanatio = Sanatio()


class SilverCalculator:
    """
    A class to represent an item for which the silver price is calculated.

    Attributes:
        weight (float): Weight of the silver item in grams.
        price_per_gram (float): Price of silver per gram.
        service_charge (float): Service charge percentage applied to the base price (default is 17%).
        tax (float): Tax percentage applied to the total price (default is 3%).
        purity (float): Purity of the silver item (default is 100% for pure silver).

    Methods:
        calculate_tax(item_price): Calculates the tax based on the given item price.
        calculate_service_charge(item_price): Calculates the service charge based on the given item price.
        calculate_base_price(): Calculates the base price based on weight, price per gram, and purity.
        calculate_price(): Calculates the total price including base price, service charge, and tax.
    """

    def __init__(self, weight, price_per_gram, service_charge=17, tax=3, purity=100):
        """
        Initializes a SilverPriceItem instance.

        Args:
            weight (float): Weight of the silver item in grams.
            price_per_gram (float): Price of silver per gram.
            service_charge (float, optional): Service charge percentage. Defaults to 17.
            tax (float, optional): Tax percentage. Defaults to 3.
            purity (float, optional): Purity of the silver item. Defaults to 100.

        Raises:
            ValueError: If any of the input values are not positive numbers or if purity is not between 0 and 100.
        """
        if weight <= 0 or price_per_gram <= 0 or service_charge < 0 or tax < 0 or not (0 <= purity <= 100):
            raise ValueError("Weight, price per gram, service charge, tax must be non-negative and purity must be between 0 and 100.")
        
        self.weight = weight
        self.price_per_gram = price_per_gram
        self.service_charge = service_charge
        self.tax = tax
        self.purity = purity

    def calculate_tax(self, item_price):
        """
        Calculates the tax based on the given item price.

        Args:
            item_price (float): The price of the item before tax.

        Returns:
            float: The tax amount.
        """
        return sanatio.truncate(item_price * self.tax / 100, 2)
        
    def calculate_service_charge(self, item_price):
        """
        Calculates the service charge based on the given item price.

        Args:
            item_price (float): The price of the item before service charge.

        Returns:
            float: The service charge amount.
        """
        return sanatio.truncate(item_price * self.service_charge / 100, 2)

    def calculate_base_price(self):
        """
        Calculates the base price of the silver item based on weight, price per gram, and purity.

        Returns:
            float: The base price.
        """
        return self.weight * self.price_per_gram * (self.purity / 100)

    def calculate_price(self):
        """
        Calculates the final price of the silver item, including base price, service charge, and tax.

        Returns:
            dict: A dictionary with the base price, service charge, service charge percentage,
                  tax, tax percentage, and final price.
        """
        base_price = self.calculate_base_price()
        service_charge = self.calculate_service_charge(base_price)
        total_price = base_price + service_charge
        tax = self.calculate_tax(total_price)
        final_price = sanatio.truncate(total_price + tax, 2)
        
        return {
            "Base Price": sanatio.truncate(base_price, 2),
            "Service Charge": sanatio.truncate(service_charge, 2),
            "Service Charge Percentage": self.service_charge,
            "Tax": sanatio.truncate(tax, 2),
            "Tax Percentage": self.tax,
            "Final Price": final_price
        }
