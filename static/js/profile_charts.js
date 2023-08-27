function statusOrdersDataChart(ordersData){
    let countNew = 0
    let countWork = 0
    let countPause = 0
    let countDone = 0
    $.each(ordersData, function (key, value) {
        if (value.order_status === 0){
            countNew += 1;
        }
        else if (value.order_status === 1) {
            countWork+= 1;
        }
        else if (value.order_status === 2) {
            countPause += 1;
        }
        else if (value.order_status === 3) {
            countDone += 1;
        }
    });
    return [countNew, countWork, countPause, countDone]
}

function typedStatusChart(statusArr, ordersData) {
    let typedStatusCTX = $('#typed_status_chart');

    let dataChart = statusOrdersDataChart(ordersData);
    let statusOrderChart = new Chart(typedStatusCTX, {
        type: 'bar',
        data: {
            labels: Object.values(statusArr),
            datasets: [{
                label: 'Количество',
                data: dataChart,
                backgroundColor: [
                    'rgba(216, 27, 96, 0.6)',
                    'rgba(3, 169, 244, 0.6)',
                    'rgba(255, 152, 0, 0.6)',
                    'rgba(29, 233, 182, 0.6)',
                ],
                borderColor: [
                    'rgba(216, 27, 96, 1)',
                    'rgba(3, 169, 244, 1)',
                    'rgba(255, 152, 0, 1)',
                    'rgba(29, 233, 182, 1)',
                ],
                borderWidth: 2
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Статистика заявок',
                    position: 'top',
                    fontSize: 16,
                    padding: 20,
                    fontColor: 'rgba(0, 0, 0, 0)'
                },
            },
            maintainAspectRatio: false,

        }
    })
}

