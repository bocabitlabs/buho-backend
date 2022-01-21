import React, { ReactElement, useEffect } from "react";
import { Bar } from "react-chartjs-2";

interface Props {
  stats: any;
}

export default function DividendsChart({ stats }: Props): ReactElement {
  const [data, setData] = React.useState<any>(null);
  const [isDataSet, setIsDataSet] = React.useState<boolean>(false);
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Dividends",
      },
    },
  };
  useEffect(() => {
    if (stats) {
      const tempData = {
        labels: [],
        datasets: [
          {
            label: "Dividends",
            data: [],
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
          {
            label: "Accum. Dividends",
            data: [],
            borderColor: "rgb(53, 162, 235)",
            backgroundColor: "rgba(53, 162, 235, 0.5)",
          },
        ],
      };
      const newYears: any = [];
      const dividends: any = [];
      const accumulatedDividends: any = [];

      stats.sort((a: any, b: any) => {
        if (a.year > b.year) {
          return 1;
        }
        if (a.year < b.year) {
          return -1;
        }
        return 0;
      });
      stats.forEach((year: any) => {
        if (
          !newYears.includes(year.year) &&
          year.sharesCount > 0 &&
          year.year !== "all" &&
          year.year !== 9999
        ) {
          newYears.push(year.year);
          dividends.push(Number(year.dividends));
          accumulatedDividends.push(Number(year.accumulatedDividends));
        }
      });
      tempData.labels = newYears;
      tempData.datasets[0].data = dividends;
      tempData.datasets[1].data = accumulatedDividends;

      setData(tempData);
      setIsDataSet(true);
    }
  }, [stats]);

  if (!isDataSet || !data) {
    return <div>Loading...</div>;
  }
  return <Bar options={options} data={data} />;
}