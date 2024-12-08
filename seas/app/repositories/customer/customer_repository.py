from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity


class CustomerRepository(metaclass=Singleton):
    entity_class = CustomerEntity

    def get_or_create_customer_by_phone_number(self, phone_number: str) -> CustomerEntity:
        customer, customer_created = self.entity_class.objects.get_or_create(phone_number=phone_number)
        return customer
