'use strict';

function orderGetReq() {
    let request = new XMLHttpRequest();
    let url = '/api-v0/orders/?';
    let param = '';

    request.open('GET', url + param, true);
    request.onload = function () {
        let data = JSON.parse(this.response);

        if (request.status >= 200 && request.status < 400) {
            console.log(data);
            let html = '<table class="pure-table"><thead><tr>' +
                '<th>Cвязь с заказчиком (id пользователя/заказчика)</th>' +
                '<th>Дата заказа</th>' +
                '<th>Cумма заказа</th>' +
                '<th></th>' +
                '</tr></thead><tbody>';
            data.results.forEach(entry => {
                html += "<tr>" +
                    "<td>" + entry.id + "</td>" +
                    "<td>" + entry.created + "</td>" +
                    "<td>" + entry.amount_price + "</td>" +
                    "<td><button onclick='del(" + entry.id + ")'>Удалить</button></td>" +
                    "</tr>";
            });
            html += "</tbody></table>";


            document.querySelector(".block-order").innerHTML = html;

        } else {
            console.log('error')
        }
    };
    request.send();
}

orderGetReq();

// ---------
function customerGetReq() {
    let req_customer = new XMLHttpRequest();
    req_customer.open('GET', '/api-v0/customers/');
    req_customer.onreadystatechange = function () {
        if (this.response !== "") {
            let data = JSON.parse(this.response);

            let html = '';
            data.forEach(entry => {
                html += "<option value='" + entry.id + "'>" + entry.title + "</option>";
            });
            document.querySelector("#select_customer").innerHTML = html;
        }
    };
    req_customer.send();
}

customerGetReq();

function del(id) {
    let req = new XMLHttpRequest();
    req.open('DELETE', '/api-v0/orders/' + id + '/');
    req.onloadend = function () {
        alert("order id: " + id + " deleted!");
        orderGetReq();
    };
    req.send();
}

function createOrder() {
    let e = document.getElementById("select_customer");
    let customer = e.options[e.selectedIndex].value;
    let amount_price = document.getElementById('amount_price').value;

    if (amount_price === "") {
        alert("Not defined amount price!");
        return false
    }

    createOrderReq(customer, amount_price);

    document.getElementById('amount_price').value = "";
    console.log(customer + " " + amount_price);
    alert("created!");
}

function createOrderReq(customer, amount_price) {
    let xhr = new XMLHttpRequest();
    let _url = "/api-v0/orders/";
    xhr.open("POST", _url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
        orderGetReq();
    };
    var data = JSON.stringify({
        "amount_price": amount_price,
        "customer": customer
    });
    xhr.send(data);
}
