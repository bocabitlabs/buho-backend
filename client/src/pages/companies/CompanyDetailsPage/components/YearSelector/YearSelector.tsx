import React, { ReactElement, useEffect, useState } from "react";
import { Form, Select } from "antd";
import StatsContent from "../StatsContent/StatsContent";
import StatsRefreshModal from "../StatsRefreshModal/StatsRefreshModal";
import { useCompanyYearStats } from "hooks/use-stats/use-company-stats";

interface Props {
  companyId: string | undefined;
  firstYear: number | null;
}

export default function YearSelector({
  companyId,
  firstYear,
}: Props): ReactElement {
  const [selectedYear, setSelectedYear] = useState<any | null>("all");
  const [years, setYears] = useState<number[]>([]);
  const [stockPrice, setStockPrice] = useState<any | null>(null);

  const { data: stats, isFetching: loadingStats } = useCompanyYearStats(
    +companyId!,
    selectedYear,
    {
      onSuccess: (data: any) => {
        setStockPrice({
          price: data.stockPriceValue,
          priceCurrency: data.stockPriceCurrency,
          transactionDate: data.stockPriceTransactionDate,
        });
      },
    },
  );

  const handleYearChange = (value: string) => {
    setSelectedYear(value);
  };

  useEffect(() => {
    async function loadInitialYears() {
      const currentYear = new Date().getFullYear();
      const newYears: number[] = [];
      if (firstYear != null) {
        for (let index = +currentYear; index >= +firstYear; index -= 1) {
          newYears.push(index);
        }
        setYears(newYears);
      }
    }
    loadInitialYears();
  }, [firstYear]);

  return (
    <div>
      <div style={{ marginTop: 16 }}>
        <Form layout="inline">
          <Select
            defaultValue={selectedYear}
            style={{ width: 120 }}
            onChange={handleYearChange}
            disabled={loadingStats}
            loading={loadingStats}
          >
            <Select.Option value="all">All</Select.Option>
            {years.map((yearItem: any) => (
              <Select.Option key={yearItem} value={yearItem}>
                {yearItem}
              </Select.Option>
            ))}
          </Select>
          <StatsRefreshModal
            companyId={companyId}
            selectedYear={selectedYear}
          />
        </Form>
      </div>
      <div style={{ marginTop: 16 }}>
        <StatsContent stats={stats} stockPrice={stockPrice} />
      </div>
    </div>
  );
}