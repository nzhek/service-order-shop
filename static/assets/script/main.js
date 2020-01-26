'use strict';

var request = new XMLHttpRequest();
var url = '/api-v0/orders-by-week/?';
var param = '';

request.open('GET', url + param, true);

request.onload = function () {
    var data = JSON.parse(this.response);

    if (request.status >= 200 && request.status < 400) {
        console.log(data);
        let html = '<table class="pure-table"><thead><tr>' +
            '<th>Дата</th>' +
            '<th>Пользователи</th>' +
            '<th>Общая сумма заказов за день</th>' +
            '</tr></thead><tbody>';
        data.orders.forEach(entry => {
            html += "<tr>" +
                "<td>" + entry.created + "</td>" +
                "<td>" + entry.customers + "</td>" +
                "<td>" + entry.amount + "</td>" +
                "</tr>";
        });
        html += "</tbody></table>";
        html += "<h3>Итог:</h3>";
        html += "<p>Заказчики: " + data.result.customers + "</p>";
        html += "<p>Сумма общая: " + data.result.amount_price + "</p>";

        document.querySelector(".block-order").innerHTML = html;

    } else {
        console.log('error')
    }
};

request.send();

function reloadOrder() {
    // request.send();
    let week = document.getElementById("select_week").value;
    let _param = new URLSearchParams("?");
    _param.set('n_week', week);
    param = _param.toString();
    request.open('GET', url + param, true);
    request.send();
}