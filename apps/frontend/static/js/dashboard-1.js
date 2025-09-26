$(function() {
    "use strict";

    // Sales Graph Top
    var ctx = document.getElementById("sales-graph-top");
    ctx.height = 100;

    var chartData = JSON.parse(document.getElementById("chart-data").textContent);

    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: "Потрачено",
                data: chartData.values, // <-- числа без $
                backgroundColor: "rgba(110, 211, 207, 0.12)",
                borderColor: "#6ed3cf",
                borderWidth: 3,
                pointBorderColor: "#6ed3cf",
                pointBackgroundColor: "#FFF",
                pointBorderWidth: 3,
                pointRadius: 5,
                pointHoverBackgroundColor: "#FFF",
                pointHoverBorderColor: "#6ed3cf",
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.yLabel + "₽"; // <-- добавляем ₽
                    }
                }
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    display: true,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    }
                }],
                yAxes: [{
                    display: true,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        min: chartData.min_val, // <-- минимальное значение
                        max: chartData.max_val, // <-- максимальное значение
                        callback: function(value) {
                            return value + "₽";
                        }
                    }
                }]
            }
        }
    });
});
