window.Telegram.WebApp.ready();
let tg = window.Telegram.WebApp;

let csrftoken = $.cookie('csrftoken');

function loadInfo() {
    let TelegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];
    let targetUrl = processUrl + '/api/person/info?TelegramId=' + TelegramId
    $.get(targetUrl).done(function(answer) {
        let data = answer.data;
        console.log(data);

        let $photo = $('#userPhoto');
        $('#person_id').val(data.person_id);
        $('#telegram_username').val(data.telegram_username);
        $('#fio').val(data.person_fio);
        $('#phone_number').val(data.phone_number);
        if (data.email != null){
            $('#email_username').val(data.email.split('@')[0]);
            $('#email_server').val(data.email.split('@')[1]);
        }
        $('#date_of_birth').val(data.person_date_of_birth);

    }).fail(function(err) {
        console.log(err);
    });
}

$(document).ready(function(){
    loadInfo();

    // SAVE EDITION
    // window.Telegram.WebApp.onEvent('mainButtonClicked', function() {
    $(document).on('click','#save_info', function(){
        let validationPerson = $('#personForm').valid();

        let telegram_id = $('#telegram_id').val();
        let person_id = $('#person_id').val();
        let person_fio = $('#fio').val();
        let phone_number = $('#phone_number').val();
        let person_date_of_birth = $('#date_of_birth').val();
        let email = $('#email_username').val() +'@'+ $('#email_server').val();

        let currentUrl = window.location.href;
        let processUrl = currentUrl.split('/profile')[0];
        let targetUrl = processUrl + '/api/person/' + person_id + '/';

        if(validationPerson) {
            $('.alert').hide();
            $.ajax({
                url: targetUrl,
                type: "PATCH",
                dataType: "json",
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Authorization': 'Telegram ' + telegram_id
                },
                traditional: true,
                data: {
                    'person_fio': person_fio,
                    'phone_number': phone_number,
                    'date_of_birth': person_date_of_birth,
                    'email': email,
                },
                success: function (response) {
                    console.log(response);
                    let result = {
                        'Save': 1,
                    };
                    tg.sendData(JSON.stringify(result));
                    tg.close();
                },
                error: function (response) {
                    console.log(response);
                }
            });
        } else {
            $('.alert').show();
        }
    });



    // WEBSOCKET
    const ws_url = `/ws/task_status/`;
    const WS = new WebSocket((location.protocol === 'https:' ? 'wss' : 'ws') + '://' + window.location.host + ws_url);

    WS.onmessage = function(e) {
            let data = JSON.parse(e.data);
            console.log(data)
    };

});