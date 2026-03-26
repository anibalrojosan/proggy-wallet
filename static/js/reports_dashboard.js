(function () {
  "use strict";

  const DOUGHNUT_COLORS = [
    "rgba(25, 135, 84, 0.75)",
    "rgba(13, 110, 253, 0.75)",
    "rgba(108, 117, 125, 0.75)",
    "rgba(255, 193, 7, 0.85)",
    "rgba(111, 66, 193, 0.75)",
    "rgba(214, 51, 132, 0.75)",
  ];

  function readPayload(elementId) {
    const el = document.getElementById(elementId);
    if (!el) {
      return null;
    }
    try {
      return JSON.parse(el.textContent);
    } catch {
      return null;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const monthlyPayload = readPayload("reports-monthly-data");
    const monthlyCanvas = document.getElementById("chart-monthly");
    if (
      monthlyPayload &&
      monthlyCanvas &&
      Array.isArray(monthlyPayload.labels) &&
      monthlyPayload.labels.length > 0 &&
      Array.isArray(monthlyPayload.datasets) &&
      monthlyPayload.datasets.length > 0
    ) {
      const ctx = monthlyCanvas.getContext("2d");
      if (ctx) {
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: monthlyPayload.labels,
            datasets: monthlyPayload.datasets.map(function (ds) {
              return {
                label: ds.label,
                data: ds.data,
                backgroundColor: ds.backgroundColor,
                borderColor: ds.borderColor,
                borderWidth: 1,
              };
            }),
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: function (value) {
                    return "$" + value;
                  },
                },
              },
            },
            plugins: {
              legend: {
                display: monthlyPayload.datasets.length > 1,
                position: "top",
              },
            },
          },
        });
      }
    }

    const typesPayload = readPayload("reports-types-data");
    const typesCanvas = document.getElementById("chart-types");
    if (
      typesPayload &&
      typesCanvas &&
      Array.isArray(typesPayload.labels) &&
      typesPayload.labels.length > 1
    ) {
      const ctx = typesCanvas.getContext("2d");
      if (ctx) {
        const n = typesPayload.data.length;
        const colors = [];
        for (let i = 0; i < n; i++) {
          colors.push(DOUGHNUT_COLORS[i % DOUGHNUT_COLORS.length]);
        }
        new Chart(ctx, {
          type: "doughnut",
          data: {
            labels: typesPayload.labels,
            datasets: [
              {
                data: typesPayload.data,
                backgroundColor: colors,
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: "bottom",
              },
            },
          },
        });
      }
    }
  });
})();
