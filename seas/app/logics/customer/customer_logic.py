from seas.app.helpers.singleton import Singleton
from seas.app.models import CustomerEntity
from seas.app.repositories.customer.customer_repository import CustomerRepository


class CustomerLogic(metaclass=Singleton):

    def __init__(self):
        self.customer_repository = CustomerRepository()

    def get_or_create_customer_by_phone_number(self, phone_number: str) -> CustomerEntity:
        return self.customer_repository.get_or_create_customer_by_phone_number(phone_number=phone_number)
