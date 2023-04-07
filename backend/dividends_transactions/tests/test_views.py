import logging
from decimal import Decimal

import factory
from companies.tests.factory import CompanyFactory
from dividends_transactions.models import DividendsTransaction
from dividends_transactions.tests.factory import DividendsTransactionFactory
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

logger = logging.getLogger("buho_backend")


class DividendsTransactionsListTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.faker_obj = Faker()

    def test_get_rights(self):
        company = CompanyFactory.create()
        url = reverse("dividends-transaction-list", args=[company.id])
        response = self.client.get(url)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        for _ in range(0, 4):
            DividendsTransactionFactory.create(
                company=company,
                gross_price_per_share_currency=company.base_currency,
                total_commission_currency=company.base_currency,
            )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class DividendsTransactionsDetailTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.company = CompanyFactory.create()
        instances = []
        for _ in range(0, 4):
            instance = DividendsTransactionFactory.create(
                company=cls.company,
                gross_price_per_share_currency=cls.company.base_currency,
                total_commission_currency=cls.company.base_currency,
            )
            instances.append(instance)
        cls.instances = instances

    def test_get_dividends(self):
        index = 0
        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[index].id])
        response = self.client.get(url)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"],
            self.instances[index].count,
        )
        self.assertEqual(
            Decimal(response.data["exchange_rate"]),
            self.instances[index].exchange_rate,
        )
        self.assertEqual(
            Decimal(response.data["total_amount"]),
            self.instances[index].total_amount.amount,
        )
        self.assertEqual(
            response.data["total_amount_currency"],
            str(self.instances[index].total_amount.currency),
        )
        index = len(self.instances) - 1
        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[index].id])
        response = self.client.get(url)
        self.assertEqual(
            Decimal(response.data["total_commission"]),
            self.instances[index].total_commission.amount,
        )
        self.assertEqual(
            response.data["total_commission_currency"],
            str(self.instances[index].total_commission.currency),
        )

    def test_update_dividends_transaction(self):
        index = 0
        temp_data = factory.build(dict, FACTORY_CLASS=DividendsTransactionFactory)
        temp_data["company"] = self.company.id
        temp_data["gross_price_per_share_currency"] = self.company.base_currency
        temp_data["total_commission_currency"] = self.company.base_currency

        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[index].id])
        response = self.client.put(url, temp_data)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Decimal(response.data["count"]),
            temp_data["count"],
        )
        self.assertEqual(
            Decimal(response.data["total_commission"]),
            temp_data["total_commission"],
        )
        self.assertEqual(
            response.data["notes"],
            temp_data["notes"],
        )

    def test_delete_transaction(self):
        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[0].id])
        response = self.client.delete(url)
        # Check status response

        trans = DividendsTransaction.objects.all()
        self.assertEqual(len(trans), 3)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(DividendsTransaction.DoesNotExist):
            DividendsTransaction.objects.get(id=self.instances[0].id)
