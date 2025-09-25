$(function() {
    "use strict";

    // Sales Graph Top
    var ctx = document.getElementById("sales-graph-top");
    ctx.height = 100;
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["2010", "2011", "2012", "2013", "2014", "2015", "2016"],
            datasets: [{
                label: "Потрачено",
                data: [28, 35, 36, 48, 46, 42, 60], // <-- числа без $
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
                        return tooltipItem.yLabel + "$"; // <-- добавляем $
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
                        callback: function(value) {
                            return value + "$"; // <-- добавляем $ на оси
                        }
                    }
                }]
            }
        }
    });
});
