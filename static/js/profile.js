window.Telegram.WebApp.ready();
let tg = window.Telegram.WebApp;
tg.MainButton.text = 'Сохранить';
tg.MainButton.show();

let csrftoken = $.cookie('csrftoken');

function loadClientInfo() {
    let TelegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];
    let targetUrl = processUrl + '/api/client/info?TelegramId=' + TelegramId
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
        $('#client_address').val(data.client_address);
        $('#addition_information').val(data.addition_information);

    }).fail(function(err) {
        console.log(err);
    });
}

function loadAgentInfo() {
    let TelegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];
    let targetUrl = processUrl + '/api/agent/info?TelegramId=' + TelegramId
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
        $('#agent_description').val(data.agent_description);
        $('#education_description').val(data.education_description);
        $('#work_experience').val(data.work_experience);
        $('#command_work').val(data.command_work);
        $('#passport_check').val(data.passport_check);
        $('#contract_work').val(data.contract_work);
        $('#guarantee_period').val(data.guarantee_period);

    }).fail(function(err) {
        console.log(err);
    });
}

function loadCompanyInfo() {
    let TelegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];
    let targetUrl = processUrl + '/api/company_by_user/info?TelegramId=' + TelegramId
    $.get(targetUrl).done(function(answer) {
        let data = answer.data;
        console.log(data);

        $('#company_id').val(data.company_id);
        $('#company_name').val(data.company_name);
        $('#legal_address').val(data.company_legal_address);
        $('#mail_address').val(data.company_mail_address);
        $('#email_address').val(data.company_email);
        $('#contact_phone').val(data.company_contact_phone);
        $('#inn').val(data.company_inn);
        $('#kpp').val(data.company_kpp);
        $('#ogrnip').val(data.company_ogrnip);
        $('#payment_account').val(data.company_payment_account);
        $('#bank').val(data.company_bank);
        $('#bik').val(data.company_bik);
        $('#okpo').val(data.company_okpo);
        $('#description').val(data.company_description);


    }).fail(function(err) {
        console.log(err);
    });
}

$(document).ready(function(){

    if ($('#agent_form').length) {
        loadAgentInfo();
    }
    else {
        loadClientInfo();
    }

    if ($('#company_form').length) {
        loadCompanyInfo();
    }


    // SAVE EDITION
    // Telegram.WebApp.onEvent('mainButtonClicked', function() {
    $(document).on('click','#save_info', function(){
        let validationPerson = $('#person_form').valid();

        let currentUrl = window.location.href;
        let processUrl = currentUrl.split('/profile')[0];

        let telegramId = $('#telegram_id').val();
        let personId = $('#person_id').val();
        let personFio = $('#fio').val();
        let phoneNumber = $('#phone_number').val();
        let personDateBirth = $('#date_of_birth').val();
        let email = $('#email_username').val() +'@'+ $('#email_server').val();
        let personData = {
            'person_fio': personFio,
            'phone_number': phoneNumber,
            'date_of_birth': personDateBirth,
            'email': email,
        }

        let additionalData = {};
        let targetPersonUrl;
        if ($('#agent_form').length) {
            targetPersonUrl = processUrl + '/api/agent/' + personId + '/';
            additionalData = {
                'agent_description': $('#agent_description').val(),
                'education_description': $('#education_description').val(),
                'work_experience': $('#work_experience').val(),
                'command_work': $('#command_work').val(),
                'contract_work': $('#contract_work').val(),
                'guarantee_period': $('#guarantee_period').val(),
            };
        }
        else {
            targetPersonUrl = processUrl + '/api/client/' + personId + '/';
            additionalData = {
                'address': $('#client_address').val(),
                'addition_information': $('#addition_information').val()
            };
        }

        if(validationPerson) {
            $('.alert').hide();
            $.ajax({
                url: targetPersonUrl,
                type: "PATCH",
                dataType: "json",
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Authorization': 'Telegram ' + telegramId
                },
                traditional: true,
                data: {...personData, ...additionalData},
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


        if ($('#company_form').length) {
            let validationCompany = $('#company_form').valid();
            let companyId = $('#company_id').val();
            let companyName =  $('#company_name').val();
            let legalAddress =  $('#legal_address').val();
            let mailAddress =  $('#mail_address').val();
            let emailAddress =  $('#email_address').val();
            let contactPhone =  $('#contact_phone').val();
            let inn =  $('#inn').val();
            let kpp =  $('#kpp').val();
            let ogrnip =  $('#ogrnip').val();
            let paymentAccount =  $('#payment_account').val();
            let bank =  $('#bank').val();
            let bik =  $('#bik').val();
            let okpo =  $('#okpo').val();
            let description =  $('#description').val();
            let targetCompanyUrl = processUrl + '/api/company/' + companyId + '/';

            if(validationCompany) {
                $('.alert').hide();
                $.ajax({
                    url: targetCompanyUrl,
                    type: "PATCH",
                    dataType: "json",
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Authorization': 'Telegram ' + telegram_id
                    },
                    traditional: true,
                    data: {
                        'name': companyName,
                        'description': description,
                        'legal_address': legalAddress,
                        'mail_address': mailAddress,
                        'inn': inn,
                        'kpp': kpp,
                        'ogrnip': ogrnip,
                        'payment_account': paymentAccount,
                        'bank': bank,
                        'bik': bik,
                        'okpo': okpo,
                        'contact_phone': contactPhone,
                        'email': emailAddress,
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
        }


    });



    // WEBSOCKET
    // const ws_url = `/ws/task_status/`;
    // const WS = new WebSocket((location.protocol === 'https:' ? 'wss' : 'ws') + '://' + window.location.host + ws_url);
    //
    // WS.onmessage = function(e) {
    //         let data = JSON.parse(e.data);
    //         console.log(data)
    // };

});