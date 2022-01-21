import React, { ReactElement } from "react";
import { Bar } from "react-chartjs-2";
import { useParams } from "react-router-dom";
import { usePortfolioAllYearStats } from "hooks/use-stats/use-portfolio-stats";

export default function ChartPortfolioDividends(): ReactElement {
  const { id } = useParams();
  const [chartData, setChartData] = React.useState<any>(null);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Portfolio Dividends",
      },
    },
  };
  function getChartData() {
    return {
      labels: [],
      datasets: [
        {
          label: "Dividends",
          data: [],
          borderColor: "rgb(255, 99, 132)",
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    };
  }
  const { isFetching: loading } = usePortfolioAllYearStats(+id!, {
    onSuccess: (responseData: any) => {
      const tempChartData = getChartData();

      const newYears: any = [];
      const dividends: any = [];

      responseData.sort((a: any, b: any) => {
        if (a.year > b.year) {
          return 1;
        }
        if (a.year < b.year) {
          return -1;
        }
        return 0;
      });
      responseData.forEach((year: any) => {
        if (
          !newYears.includes(year.year) &&
          year.year !== "all" &&
          year.year !== 9999
        ) {
          newYears.push(year.year);
          dividends.push(Number(year.dividends));
        }
      });
      tempChartData.labels = newYears;
      tempChartData.datasets[0].data = dividends;

      setChartData(tempChartData);
    },
  });

  if (!chartData || loading) {
    return <div>Loading...</div>;
  }
  return <Bar options={options} data={chartData} />;
}