window.Telegram.WebApp.ready();
let tg = window.Telegram.WebApp;
tg.MainButton.text = 'Сохранить';
tg.MainButton.show();

let csrftoken = $.cookie('csrftoken');

function openDiv(elem_id_to_open) {
    formOpened = $(`#${ elem_id_to_open }`)
    if (formOpened.hasClass('show')) {
        formOpened.removeClass('show', 2000);
    }
    else {
        formOpened.addClass('show', 2000);
    }

};

function loadClientInfo(TelegramId, currentUrl, processUrl) {
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

function loadAgentInfo(TelegramId, currentUrl, processUrl) {
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

function loadCompanyInfo(TelegramId, currentUrl, processUrl) {
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

function loadOrderInfo(TelegramId, currentUrl, processUrl) {
    let targetUrl = processUrl + '/api/orders_by_agent/info?TelegramId=' + TelegramId
    $.get(targetUrl).done(function(answer) {
        let listData = JSON.parse(answer.data);
        console.log(listData);

        let statusArr = {
                0: 'Не в работе',
                1: 'В работе',
                2: 'Приостановлена',
                3: 'Выполнена',
        }
        let countStrAll = 1;
        $.each(listData,function(key,value) {
            console.log(value);
            // Новые заявки
            let table = $('#analytic_table')
            if (value.order_status === 0) {
                let checkedValue = (value.order_control) ? "checked" : "";
                let countStr=$('table tr[data-status=new]').length + 1;
                table.append(
                    `<tr data-status="new" style="display: none;">` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${countStr} </p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p">` +
                                `<a href="#">${value.order_id} </a>` +
                            `</p>` +
                        `</td>` +
                        `<td>` +
                            `<input class="form-check-input" type="checkbox" value="" id="flexCheckChecked"  ${checkedValue}>` +
                            `<label class="form-check-label" htmlFor="flexCheckChecked"> </label>` +
                        `</td>` +
                    `</tr>`
                 );
            }
            else if (value.order_status === 1) {
                let countStr=$('table tr[data-status=in_work]').length + 1;
                let deadline = moment(new Date(value.order_deadline)).format('hh:mm - DD.MM.YY');
                console.log(deadline)
                table.append(
                    `<tr data-status="in_work" style="display: none;">` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${countStr} </p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p">` +
                                `<a href="#">${value.order_id} </a>` +
                            `</p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p">` +
                                `<a href="tg://user?id=${value.order_client_tg}""> <img class="tg_icon" src="${srcTgIcon}"></a>` +
                            `</p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${deadline} </p>` +
                        `</td>` +
                    `</tr>`
                 );
            }
            else if (value.order_status === 2){
                let countStr=$('table tr[data-status=pause]').length + 1;
                table.append(
                    `<tr data-status="pause" style="display: none;">` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${countStr} </p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p">` +
                                `<a href="tg://user?id=${value.order_client_tg}""> <img class="tg_icon" src="${srcTgIcon}"></a>` +
                            `</p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${statusArr[value.order_status]} </p>` +
                        `</td>` +
                    `</tr>`
                 );
            }
            else {
                let countStr=$('table tr[data-status=pause]').length + 1;
                let start_time = moment(new Date(value.order_start_time)).format('hh:mm - DD.MM.YY');
                let end_time = moment(new Date(value.order_end_time)).format('hh:mm - DD.MM.YY');
                table.append(
                    `<tr data-status="done" style="display: none;">` +
                        `<td>` +
                            `<p class="text-center table-lc-p"> ${countStr} </p>` +
                        `</td>` +
                        `<td class="text-center">` +
                            `<p class="text-center table-lc-p"> ${start_time} <b> / </b> ${end_time}</p>` +
                        `</td>` +
                        `<td class="text-center">` +
                            `<p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>` +
                        `</td>` +
                        `<td>` +
                            `<p class="text-center table-lc-p">` +
                                `<a href="#">${value.order_id} </a>` +
                            `</p>` +
                        `</td>` +
                    `</tr>`
                );
            }
            table.append(
                `<tr data-status="all">` +
                    `<td>` +
                        `<p class="text-center table-lc-p"> ${countStrAll} </p>` +
                    `</td>` +
                    `<td class="text-center">` +
                        `<p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>` +
                    `</td>` +
                    `<td>` +
                        `<p class="text-center table-lc-p">` +
                            `<a href="tg://user?id=${value.order_client_tg}""> <img class="tg_icon" src="${srcTgIcon}"></a>` +
                        `</p>` +
                    `</td>` +
                    `<td>` +
                        `<p class="text-center table-lc-p"> ${statusArr[value.order_status]} </p>` +
                    `</td>` +
                `</tr>`
            );
            countStrAll += 1;
        });
        //  'order_id'
        // 'order_name'
        // 'order_price'
        // 'order_deadline'
        // 'order_info'
        // 'order_control'
        // 'order_status'
        // 'order_product_type'
        // 'order_product_info'
        // 'order_client_tg'

        // $('#company_id').val(data.company_id);


    }).fail(function(err) {
        console.log(err);
    });
}

$(document).ready(function(){
    let TelegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];

    $('.btn-filter').on('click', function () {
          let $target = $(this).data('target');
          $('.table thead').css('display', 'none');
          $('.table tr[data-status]').css('display', 'none');
          $('.table tr[data-status="' + $target + '"]').fadeIn('slow');
          $('.table thead[data-status="' + $target + '"]').fadeIn('slow');
        });

    if ($('#agent_form').length) {
        loadAgentInfo(TelegramId, currentUrl, processUrl);
        loadOrderInfo(TelegramId, currentUrl, processUrl)
    }
    else {
        loadClientInfo(TelegramId, currentUrl, processUrl);
    }

    if ($('#company_form').length) {
        loadCompanyInfo(TelegramId, currentUrl, processUrl);
    }


    // SAVE INFO
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