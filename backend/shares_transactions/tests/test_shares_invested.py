import datetime
import logging
from decimal import Decimal
from functools import reduce

from faker import Faker

from buho_backend.tests.base_test_case import BaseApiTestCase
from buho_backend.transaction_types import TransactionType
from companies.tests.factory import CompanyFactory
from shares_transactions.calculators.shares_transaction_calculator import SharesTransactionCalculator
from shares_transactions.tests.factory import SharesTransactionFactory

logger = logging.getLogger("buho_backend")


class SharesInvestedTestCase(BaseApiTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.faker_obj = Faker()
        # Create company
        # Add shares
        cls.company = CompanyFactory.create()
        cls.shares_count = 0
        cls.total_amount = 0
        cls.total_transactions = 0
        cls.years = [2018, 2020, 2021, datetime.date.today().year]
        cls.counts = [1, 2, 3, 4]
        cls.totalAmounts = [1, 2, 3, 4]
        cls.accumulated_counts = [1, 3, 6, 10]
        cls.prices = [Decimal(1), Decimal(2), Decimal(3), Decimal(4)]
        cls.exchange_rate = 0.5
        cls.commissions = [Decimal(1), Decimal(2), Decimal(3), Decimal(4)]
        cls.prices_times_counts = [
            1 * cls.exchange_rate,  # 50.5
            2 * cls.exchange_rate,  # 201
            3 * cls.exchange_rate,  # 451.5
            4 * cls.exchange_rate,  # 802
        ]
        for index in range(0, len(cls.years)):
            first_datetime = datetime.datetime.strptime(f"{cls.years[index]}-01-01", "%Y-%m-%d")
            SharesTransactionFactory.create(
                company=cls.company,
                gross_price_per_share_currency=cls.company.base_currency,
                total_commission_currency=cls.company.base_currency,
                count=cls.counts[index],
                type=TransactionType.BUY,
                gross_price_per_share=cls.prices[index],
                exchange_rate=cls.exchange_rate,
                total_commission=cls.commissions[index],
                transaction_date=datetime.date(first_datetime.year, first_datetime.month, first_datetime.day),
            )
            cls.shares_count += cls.counts[index]
            cls.total_transactions += 1

    # def setUp(self):
    #     pass

    def test_calculate_invested_on_year(self):
        index = 3
        utils = SharesTransactionCalculator(self.company.shares_transactions)
        self.assertEqual(
            utils.calculate_invested_on_year(self.years[index]),
            self.prices_times_counts[index],
        )

        index = 0
        utils = SharesTransactionCalculator(self.company.shares_transactions)
        self.assertEqual(
            utils.calculate_invested_on_year(self.years[index]),
            self.prices_times_counts[index],
        )

    def test_get_accumulated_investment_until_current_year(self):
        index = 3
        utils = SharesTransactionCalculator(self.company.shares_transactions)
        self.assertEqual(
            utils.get_accumulated_investment_until_current_year(),
            reduce(lambda a, b: a + b, self.prices_times_counts[: index + 1]),
        )

    def test_calculate_invested_on_year_all(self):
        index = 3
        utils = SharesTransactionCalculator(
            self.company.shares_transactions,
        )
        self.assertEqual(
            utils.calculate_invested_on_year(self.years[index]),
            self.prices_times_counts[index],
        )

    def test_get_accumulated_investment_on_year(self):
        index = 3
        utils = SharesTransactionCalculator(
            self.company.shares_transactions,
        )
        self.assertEqual(
            utils.calculate_accumulated_investment_until_year(self.years[index]),
            reduce(lambda a, b: a + b, self.prices_times_counts[: index + 1]),
        )
        index = 1
        utils = SharesTransactionCalculator(
            self.company.shares_transactions,
        )
        self.assertEqual(
            utils.calculate_accumulated_investment_until_year(self.years[index]),
            reduce(lambda a, b: a + b, self.prices_times_counts[: index + 1]),
        )
