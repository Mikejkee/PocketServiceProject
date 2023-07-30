window.Telegram.WebApp.ready();
let tg = window.Telegram.WebApp;

let csrftoken = $.cookie('csrftoken');


$(document).ready(function(){

    // WEBSOCKET
    const ws_url = `/ws/task_status/`;
    const WS = new WebSocket((location.protocol === 'https:' ? 'wss' : 'ws') + '://' + window.location.host + ws_url);

    WS.onmessage = function(e) {
            let data = JSON.parse(e.data);
            let message = JSON.parse(data['message']);
            console.log(message)

            let html_text = '';
            let telegram_id = parseInt($('#telegram_id').val());

            if(message.length !== 0) {
                message.forEach((element) => {
                    console.log(element);
                });
            }

    };

});