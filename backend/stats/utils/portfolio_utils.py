import datetime
from itertools import groupby
import logging
from django.contrib.auth.models import User
from buho_backend.transaction_types import TransactionType
from stats.models.portfolio_stats import PortfolioStatsForYear
from stats.utils.company_utils import CompanyStatsUtils, CompanyUtils
from stock_prices.api import StockPricesApi
from stock_prices.services.custom_yfinance_service import CustomYFinanceService
from portfolios.models import Portfolio
from shares_transactions.models import SharesTransaction
from dividends_transactions.models import DividendsTransaction

logger = logging.getLogger("buho_backend")


class PortfolioUtils:
    def get_portfolio_first_year(self, portfolio_id, user_id):
        query = SharesTransaction.objects.filter(
            company__portfolio=portfolio_id, user=user_id
        ).order_by("transaction_date")
        if query.exists():
            return query[0].transaction_date.year
        return None

class PortfolioStatsUtils:
    def __init__(
        self, portfolio_id, user_id, year="all", use_currency="portfolio", force=False
    ):
        self.portfolio = Portfolio.objects.get(id=portfolio_id, user=user_id)
        self.year = year
        self.use_currency = use_currency
        self.user_id = user_id
        self.force = force

    def _get_total_invested_in_rights(self):
        total = 0
        for company in self.portfolio.companies.all():
            query = company.rights_transactions
            if self.year == "all":
                query = query.all()
            else:
                query = query.filter(
                    transaction_date__year=self.year,
                    type=TransactionType.BUY,
                )
            for item in query:
                exchange_rate = 1
                if self.use_currency == "portfolio":
                    exchange_rate = item.exchange_rate
                total += (
                    item.gross_price_per_share.amount * item.count * exchange_rate
                    + item.total_commission.amount * exchange_rate
                )
        return total

    def _get_total_invested_in_shares(self):
        total = 0
        for company in self.portfolio.companies.all():

            query = company.shares_transactions
            if self.year == "all":
                query = query.filter(type=TransactionType.BUY)
            else:
                query = query.filter(
                    transaction_date__year=self.year, type=TransactionType.BUY
                )
            for item in query:
                exchange_rate = 1
                if self.use_currency == "portfolio":
                    exchange_rate = item.exchange_rate
                total += (
                    item.gross_price_per_share.amount * exchange_rate * item.count
                    + item.total_commission.amount * exchange_rate
                )
        return total

    def _get_accumulated_invested_in_shares_until_year(self):
        total = 0
        for company in self.portfolio.companies.all():
            query = company.shares_transactions
            if self.year == "all":
                query = query.filter(type=TransactionType.BUY)
            else:
                query = query.filter(
                    transaction_date__year__lte=self.year, type=TransactionType.BUY
                )
            for item in query:
                exchange_rate = 1
                if self.use_currency == "portfolio":
                    exchange_rate = item.exchange_rate
                total += (
                    item.gross_price_per_share.amount * exchange_rate * item.count
                    + item.total_commission.amount * exchange_rate
                )
        return total

    def _get_accumulated_invested_in_rights_until_year(self):
        total = 0
        for company in self.portfolio.companies.all():
            query = company.rights_transactions
            if self.year == "all":
                query = query.filter(type=TransactionType.BUY)
            else:
                query = query.filter(
                    transaction_date__year__lte=self.year, type=TransactionType.BUY
                )
            for item in query:
                exchange_rate = 1
                if self.use_currency == "portfolio":
                    exchange_rate = item.exchange_rate
                total += (
                    item.gross_price_per_share.amount * exchange_rate * item.count
                    + item.total_commission.amount * exchange_rate
                )
        return total

    def get_dividends(self):
        total = 0
        for company in self.portfolio.companies.all():
            query = company.dividends_transactions
            if self.year == "all":
                query = query.all()
            else:
                query = query.filter(transaction_date__year=self.year)
            for item in query:
                exchange_rate = 1
                if self.use_currency == "portfolio":
                    exchange_rate = item.exchange_rate
                total += (
                    item.gross_price_per_share.amount * exchange_rate * item.count
                    + item.total_commission.amount * exchange_rate
                )
        return total

    def get_accumulated_dividends_until_year(self):
        total = 0
        for company in self.portfolio.companies.all():
            query = company.dividends_transactions
            if self.year == "all":
                query = query.all()
            else:
                query = query.filter(transaction_date__year__lte=self.year)
            for item in query:
                exchange_rate = 1
                if self.use_currency == "portfolio":
                    exchange_rate = item.exchange_rate
                total += (
                    item.gross_price_per_share.amount * exchange_rate * item.count
                    + item.total_commission.amount * exchange_rate
                )
        return total

    def get_total_invested(self):
        total = 0
        total += self._get_total_invested_in_shares()
        total += self._get_total_invested_in_rights()
        return total

    def get_accumulated_investment_until_year(self):
        total = 0
        total += self._get_accumulated_invested_in_shares_until_year()
        total += self._get_accumulated_invested_in_rights_until_year()
        return total

    def get_portfolio_value(self):
        total = 0
        logger.debug("Get portfolio value")
        for company in self.portfolio.companies.all():
            if company.is_closed:
                continue

            first_year = CompanyUtils().get_company_first_year(company.id, company.user)
            logger.debug(f"{company.name} First year: {first_year} vs {self.year}")
            if self.year != "all":
                if not first_year or first_year > int(self.year):
                    total += 0
                    continue

            company_stats = CompanyStatsUtils(
                company.id, self.user_id, self.year, use_currency=self.use_currency
            )
            shares_count = company_stats.get_shares_count()
            api_service = CustomYFinanceService()
            api = StockPricesApi(api_service)
            if self.year == "all":
                stock_price = api.get_last_data_from_last_month(company.ticker)
            else:
                stock_price = api.get_last_data_from_year(company.ticker, self.year)
            portfolio_value = company_stats.get_portfolio_value(
                stock_price, shares_count
            )
            total += portfolio_value
        return total

    def get_return_with_dividends(
        self, portfolio_value, accumulated_dividends, total_invested
    ):
        if portfolio_value:
            return portfolio_value - total_invested + accumulated_dividends
        return 0

    def get_return(self, portfolio_value, total_invested):
        if portfolio_value:
            return portfolio_value - total_invested
        return 0

    def get_return_percent(self, total_return, total_invested):
        if total_invested != 0:
            return total_return / total_invested * 100
        return 0

    def get_stats_for_year(self):

        year_for_all = 9999
        temp_year = year_for_all if self.year == "all" else self.year

        if PortfolioStatsForYear.objects.filter(
            portfolio=self.portfolio, year=temp_year
        ).exists():
            results = PortfolioStatsForYear.objects.get(
                portfolio=self.portfolio, year=temp_year
            )
            return results

        data = {
            "invested": 0,
            "dividends": 0,
            "dividends_yield": 0,
            "portfolio_currency": self.portfolio.base_currency,
            "accumulated_investment": 0,
            "accumulated_dividends": 0,
            "portfolio_value": 0,
        }

        for company in self.portfolio.companies.all():
            if company.is_closed:
                continue

            company_stats = CompanyStatsUtils(
                company.id, self.user_id, year=self.year, force=self.force
            )
            instance = company_stats.get_stats_for_year()
            data["invested"] += instance.invested
            data["dividends"] += instance.dividends
            data["accumulated_investment"] += instance.accumulated_investment
            data["accumulated_dividends"] += instance.accumulated_dividends
            data["portfolio_value"] += instance.portfolio_value

        data["return_value"] = self.get_return(
            data["portfolio_value"], data["accumulated_investment"]
        )
        data["return_percent"] = self.get_return_percent(
            data["return_value"], data["accumulated_investment"]
        )
        data["return_with_dividends"] = self.get_return_with_dividends(
            data["portfolio_value"],
            data["accumulated_dividends"],
            data["accumulated_investment"],
        )
        data["return_with_dividends_percent"] = self.get_return_percent(
            data["return_with_dividends"], data["accumulated_investment"]
        )

        data["dividends_yield"] = self.get_dividends_yield(
            data["dividends"], data["portfolio_value"]
        )

        # Create a new CompanyStatsForYear
        data = PortfolioStatsForYear.objects.create(
            user=User.objects.get(id=self.user_id),
            portfolio=self.portfolio,
            year=temp_year,
            **data,
        )

        return data

    def get_stats_for_year_by_company(self):
        results = []
        for company in self.portfolio.companies.all():
            company_stats = CompanyStatsUtils(
                company.id, self.user_id, year=self.year, force=self.force
            )
            instance = company_stats.get_stats_for_year()
            results.append(instance)

        return results

    def get_portfolio_first_year(self):
        transactions = SharesTransaction.objects.filter(
            company__portfolio=self.portfolio.id, user=self.user_id
        )
        first_year = transactions.order_by("transaction_date").first()
        if not first_year:
            return None
        return_value = {"year": first_year.transaction_date.year}
        return return_value

    def get_dividends_yield(self, dividends, portfolio_value):
        if portfolio_value != 0:
            return dividends / portfolio_value * 100 if portfolio_value else 0
        return 0

    def get_all_years_stats(self):
        years_result = []
        years_array = []
        first_year = self.get_portfolio_first_year()
        # Get years between year and current year
        if first_year:
            first_year = first_year["year"]
            years_array = range(int(first_year), datetime.datetime.now().year + 1)

        for year in years_array:
            data = {
                "year": year,
                "invested": 0,
                "dividends": 0,
                "portfolioCurrency": self.portfolio.base_currency,
                "accumulatedInvestment": 0,
                "accumulatedDividends": 0,
                "portfolioValue": 0,
                "dividendsYield": 0,
            }

            for company in self.portfolio.companies.all():
                company_stats = CompanyStatsUtils(company.id, self.user_id, year=year)
                instance = company_stats.get_stats_for_year()
                data["invested"] += instance.invested
                data["dividends"] += instance.dividends
                data["accumulatedInvestment"] += instance.accumulated_investment
                data["accumulatedDividends"] += instance.accumulated_dividends
                data["portfolioValue"] += instance.portfolio_value

            data["returnValue"] = self.get_return(
                data["portfolioValue"], data["accumulatedInvestment"]
            )
            data["returnPercent"] = self.get_return_percent(
                data["returnValue"], data["accumulatedInvestment"]
            )
            data["return_with_dividends"] = self.get_return_with_dividends(
                data["portfolioValue"],
                data["accumulatedDividends"],
                data["accumulatedInvestment"],
            )
            data["return_with_dividends_percent"] = self.get_return_percent(
                data["return_with_dividends"], data["accumulatedInvestment"]
            )

            data["dividendsYield"] = self.get_dividends_yield(
                data["dividends"], data["portfolioValue"]
            )

            years_result.append(data)

        return years_result

    def get_dividends_for_year_monthly(self, year=None):
        logger.debug(f"Get dividends for year {year}")
        if year == None:
            year = self.year
        transactions = (
            DividendsTransaction.objects.filter(
                company__portfolio=self.portfolio, transaction_date__year=year
            )
            .only(
                "transaction_date",
                "gross_price_per_share",
                "gross_price_per_share_currency",
                "exchange_rate",
                "count",
            )
            .order_by("transaction_date")
        )
        summary = {
            k: sum(
                (x.count * x.exchange_rate * x.gross_price_per_share.amount) for x in g
            )
            for k, g in groupby(transactions, key=lambda i: i.transaction_date.month)
        }
        return summary

    def get_dividends_for_all_years_monthly(self):
        logger.debug(f"Get dividends for all years monthly")
        years = {}
        first_year = PortfolioUtils().get_portfolio_first_year(
            self.portfolio, self.user_id
        )

        # Iterate all years until today
        for year in range(first_year, datetime.datetime.now().year + 1):
            years[year] = self.get_dividends_for_year_monthly(year)
        return years