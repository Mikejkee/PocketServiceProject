window.Telegram.WebApp.ready();
let tg = window.Telegram.WebApp;
tg.MainButton.text = 'Сохранить';
tg.MainButton.show();

let csrftoken = $.cookie('csrftoken');


function openDiv(elemIdToOpen) {
    let formOpened = $(`#${elemIdToOpen}`)
    if (formOpened.hasClass('show')) {
        formOpened.removeClass('show');
    } else {
        formOpened.addClass('show');
    }
}

function editStrInfo(elem) {
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];
    let telegramId = $('#telegram_id').val();

    let row = $(elem).closest('tr');
    let thead = $(`thead[data-status=${row.attr('data-status')}]`).find('th')
    let cells = row.find('td');

    // Создание формы для редактирования ячеек
    let closeButton = $(`<button type="button" class="btn-close close-form" aria-label="Close"></button>`)
    let inputForm = $(`<div class="container edit-form"> <form id="editForm">`).append(closeButton);
    thead.each(function (index, value) {
        let theadId = $(value).prop('id');
        if (theadId !== "") {
            inputForm.append(
                `<div class="mb-3">
                    <label class="form-label" for="${theadId}">${$(value).text()}:</label>
                    <input class="form-control" type="text" id="${theadId}" value="${$(cells[index]).text().trim()}">
                </div>`
            )
        }
    });
    let saveButton = $('<input class="btn btn-primary" type="submit" value="Сохранить">');
    inputForm.append(saveButton);
    inputForm.append(`</form> </div>`);

    saveButton.click(function () {
        let editedData = {};
        let targetEditUrl;
        editedData['EducationId'] = row.attr('education-id')
        if (editedData['EducationId'] !== undefined) {
            targetEditUrl = processUrl + '/api/education_by_agent/edit'
        } else {
            editedData['PriceId'] = row.attr('price-id')
            targetEditUrl = processUrl + '/api/prices_by_agent/edit'
        }


        inputForm.find('input[class="form-control"]').each(function (key, value) {
            editedData[$(this).prop('id')] = $(this).val();
            $(cells[key]).text($(value).val())
        });


        if ($('#editForm').valid()) {
            $('.alert').hide();
            $.ajax({
                url: targetEditUrl,
                type: "POST",
                dataType: "json",
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Authorization': 'Telegram ' + telegramId
                },
                traditional: true,
                data: editedData,
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

        inputForm.hide(100);
        $('.overlay').hide();
        inputForm.remove()
    });

    closeButton.click(function () {
        inputForm.hide(100)
        $('.overlay').hide();
        inputForm.remove()
    });


    // Добавление формы для редактирования в строку таблицы
    $('#main-div').append(inputForm);
    $('.overlay').show();
    $('.edit-form').show(100);
}

function loadAgentInfo(TelegramId, currentUrl, processUrl) {
    let targetUrl = processUrl + '/api/agent/info?TelegramId=' + TelegramId
    let targetPricesUrl = processUrl + '/api/prices_by_agent/info?AgentId='
    let targetEducationUrl = processUrl + '/api/education_by_agent/info?AgentId='
    let targetCommentUrl = processUrl + '/api/comments_by_agent/info?AgentId='

    $.get(targetUrl).done(function (answer) {
        let data = answer.data;
        console.log(data);

        let $photo = $('#userPhoto');
        $('#person_id').val(data.person_id);
        $('#telegram_username').val(data.telegram_username);
        $('#fio').val(data.person_fio);
        $('#phone_number').val(data.phone_number);
        if (data.email != null) {
            $('#email_username').val(data.email.split('@')[0]);
            $('#email_server').val(data.email.split('@')[1]);
        }
        $('#date_of_birth').val(data.person_date_of_birth);
        $('#agent_description').val(data.agent_description);
        // $('#education_description').val(data.education_description);
        $('#work_experience').val(data.work_experience);
        if (data.command_work === true) {
            $('#command_work').attr('checked', '')
        }
        if (data.passport_check === true) {
            $('#passport_check').attr('checked', '')
        }
        if (data.contract_work === true) {
            $('#contract_work').attr('checked', '')
        }
        $('#guarantee_period').val(data.guarantee_period);

        // Загрузка цен и услуг агента
        let table = $(`#agent_${data.telegram_id}_tbody`)
        $.get(targetPricesUrl + data.person_id).done(function (answer) {
            let listPrices = JSON.parse(answer.data);
            console.log(listPrices);

            $.each(listPrices, function (typeProduct, products) {
                table.append(
                    `<tr class="table-group-divide table-dark" data-status="products">
                            <td colspan="3">
                                <p class="text-center table-lc-p" style="margin-bottom: 0px;"> ${typeProduct} </p>
                            </td>
                        </tr>`
                );
                $.each(products, function (type_info, price_info) {
                    table.append(
                        `<tr data-status="products" price-id="${price_info[1]}" product-id="${price_info[2]}">
                            <td>
                                <p class="text-center table-lc-p order-info" style="margin-bottom: 0px;" > ${type_info} </p>
                            </td>
                            <td>
                                <p class="text-center table-lc-p" style="margin-bottom: 0px;" > ${price_info[0]}</p>
                            </td>
                            <td>
                                <p class="text-center table-lc-p">
                                    <img class="edit-btn my_icons_sm" onclick="editStrInfo(this)" src="${srcEdit}"></a>
                                    <img class="delete-btn my_icons_sm" src="${srcCancel}"></a>
                                </p>
                            </td>
                        </tr>`
                    );
                })
            })
        })

        // Загрузка образования агента
        $.get(targetEducationUrl + data.person_id).done(function (answer) {
            let listEducations = JSON.parse(answer.data);
            console.log(listEducations);

            $.each(listEducations, function (key, educationInfo) {
                let EducationChecked = ''
                if (educationInfo.EducationChecked === true) {
                    EducationChecked = 'checked="checked"'
                }
                table.append(
                    `<tr data-status="education" education-id="${educationInfo.EducationId}" style="display: none;">
                        <td>
                            <p class="text-center table-lc-p"> ${educationInfo.UniversityName} </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p"> ${educationInfo.SpecializationName}</p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p"> ${educationInfo.EducationEnd}</p>
                        </td>
                        <td>
                            <input class="form-check-input" type="checkbox" value="" id="educationChecked"  ${EducationChecked} disabled>
                            <label class="form-check-label" htmlFor="educationChecked"> </label>    
                        </td>
                        <td>
                            <p class="text-center table-lc-p">
                                <img class="edit-btn my_icons_sm" onclick="editStrInfo(this)" src="${srcEdit}"></a>
                                <img class="delete-btn my_icons_sm" src="${srcCancel}"></a>
                            </p>
                        </td>
                    </tr>`
                );
            })
        })

        // Загрузка комментариев
        $.get(targetCommentUrl + data.person_id).done(function (answer) {
            let listComments = JSON.parse(answer.data);
            console.log(listComments);

            $.each(listComments, function (key, commentInfo) {
                table.append(
                    `<tr data-status="feedback" style="display: none;">
                        <td>
                            <p class="text-center table-lc-p" id="raiting_${commentInfo.id}" style="margin: 0 auto 0 auto"></p>
                            <p class="text-center table-lc-p"> ${commentInfo.data} </p>
                        </td>
                        <td>
                            <p class="table-lc-p" style="text-align:left;"> <b> ${commentInfo.client} </b></p>
                            <p class="table-lc-p" style="text-align:left; color: gray"> <i> ${commentInfo.product} </i></p>
                            <p class="comment_text"> ${commentInfo.text}</p>
                            <p class="text-center table-lc-p" id="images_${commentInfo.id}"></p>
                        </td>
                    </tr>`
                );
                $(`#raiting_${commentInfo.id}`).rateYo({
                    rating: commentInfo.rating,
                    starWidth: '17px',
                    readOnly: true,
                });
                $.each(commentInfo.images, function (key, img) {
                    $(`#images_${commentInfo.id}`).append(
                        `<a data-fancybox="images" 
                             data-src="${img}" 
                             data-caption="${commentInfo.text} class="comment_img_full">
                            <img class="comment_img" src="${img}">
                         </a>`
                    )
                });
            })
        })

    }).fail(function (err) {
        console.log(err);
    });


}

function loadCompanyInfo(TelegramId, currentUrl, processUrl) {
    let targetUrl = processUrl + '/api/company_by_user/info?TelegramId=' + TelegramId
    $.get(targetUrl).done(function (answer) {
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


    }).fail(function (err) {
        console.log(err);
    });
}

function loadOrderInfo(targetUrl, statusArr) {
    // TODO: Сделать контактную возможность не только в тг, а еслит нет юзернейма у пользователя, то по телефону
    $.get(targetUrl).done(function (answer) {
        let listData = JSON.parse(answer.data);
        console.log(listData);

        let countStrAll = 1;
        let table = $('#analytic_table')
        $.each(listData, function (key, value) {
            // Заявки по типам
            if (value.order_status === 0) {
                let checkedValue = (value.order_control) ? "checked" : "";
                let countStr = $('table tr[data-status=new]').length + 1;
                table.append(
                    `<tr data-status="new" style="display: none;">
                        <td>
                            <p class="text-center table-lc-p"> ${countStr} </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p">
                                <a href="#">${value.order_id} </a>
                            </p>
                        </td>
                        <td>
                            <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked"  ${checkedValue}>
                            <label class="form-check-label" htmlFor="flexCheckChecked"> </label>
                        </td>
                    </tr>`
                );
            } else if (value.order_status === 1) {
                let countStr = $('table tr[data-status=in_work]').length + 1;
                let deadline = moment(new Date(value.order_deadline)).format('hh:mm - DD.MM.YY');
                console.log(deadline)
                table.append(
                    `<tr data-status="in_work" style="display: none;">
                        <td>
                            <p class="text-center table-lc-p"> ${countStr} </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p">
                                <a href="#">${value.order_id} </a>
                            </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p">
                                <a href="https://t.me/${value.order_contact_tg}"> <img class="tg_icon" src="${srcTgIcon}"></a>
                            </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p"> ${deadline} </p>
                        </td>
                    </tr>`
                );
            } else if (value.order_status === 2) {
                let countStr = $('table tr[data-status=pause]').length + 1;
                table.append(
                    `<tr data-status="pause" style="display: none;">
                        <td>
                            <p class="text-center table-lc-p"> ${countStr} </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p">
                                <a href="https://t.me/${value.order_contact_tg}"> <img class="tg_icon" src="${srcTgIcon}"></a>
                            </p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p"> ${statusArr[value.order_status]} </p>
                        </td>
                    </tr>`
                );
            } else {
                let countStr = $('table tr[data-status=done]').length + 1;
                let start_time = moment(new Date(value.order_start_time)).format('hh:mm - DD.MM.YY');
                let end_time = moment(new Date(value.order_end_time)).format('hh:mm - DD.MM.YY');
                table.append(
                    `<tr data-status="done" style="display: none;">
                        <td>
                            <p class="text-center table-lc-p"> ${countStr} </p>
                        </td>
                        <td class="text-center">
                            <p class="text-center table-lc-p"> ${start_time} <b> / </b> ${end_time}</p>
                        </td>
                        <td class="text-center">
                            <p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>
                        </td>
                        <td>
                            <p class="text-center table-lc-p">
                                <a href="#">${value.order_id} </a>
                            </p>
                        </td>
                    </tr>`
                );
            }
            table.append(
                `<tr data-status="all">
                    <td>
                        <p class="text-center table-lc-p"> ${countStrAll} </p>
                    </td>
                    <td class="text-center">
                        <p class="text-center table-lc-p"> ${value.order_product_type} <b> / </b> ${value.order_price}</p>
                    </td>
                    <td>
                        <p class="text-center table-lc-p">
                            <a href="https://t.me/${value.order_contact_tg}"> <img class="tg_icon" src="${srcTgIcon}"></a>
                        </p>
                    </td>
                    <td>
                        <p class="text-center table-lc-p"> ${statusArr[value.order_status]} </p>
                    </td>
                </tr>`
            );
            countStrAll += 1;
        });

        typedStatusChart(statusArr, listData);

    }).fail(function (err) {
        console.log(err);
    });
}

$(document).on("click", "a", function () {
    let href = $(this).attr('href');
    if (href.indexOf('tg') === 0) {
        tg.openTelegramLink(href);
    }
});

$(document).ready(function () {
    let telegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/profile')[0];

    let statusArr = {
        0: 'Не в работе',
        1: 'В работе',
        2: 'Приостановлена',
        3: 'Выполнена',
    }
    if ($('#agent_form').length) {
        loadAgentInfo(telegramId, currentUrl, processUrl);
        let targetUrl = processUrl + '/api/orders_by_agent/info?TelegramId=' + telegramId
        loadOrderInfo(targetUrl, statusArr);

        $('#createInfo').click(function () {
            let theadData = $(`#agent_${telegramId}_table`).find('thead:visible').attr('data-status')

            // Создание формы
            let formfield = ""
            if (theadData === 'products') {
                formfield =
                    `<div class="mb-3">
                        <label class="form-label" for="typeProduct">Тип услуги:</label>
                        <select class="form-select" id="typeProduct">
                            <option selected>Выберите тип услуги</option>
                            <option value="0">Ремонт квартиры</option>
                            <option value="1">Ремонт техники</option>
                            <option value="2">Ремонт мебели</option>
                            <option value="3">Услуги красоты</option>
                            <option value="4">Уборка</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="productInfo">Описание услуги:</label>
                        <input class="form-control" type="text" id="productInfo" placeholder="Выравнивание стен, пола и т.д.">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="productPrice">Цена за услугу:</label>
                        <input class="form-control" type="text" id="productPrice">
                    </div>`
            } else {
                formfield =
                    `<div class="mb-3">
                        <label class="form-label" for="universityCountry">Страна обучения:</label>
                        <input class="form-control" type="text" id="universityCountry">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="universityTown">Город обучения:</label>
                        <input class="form-control" type="text" id="universityTown">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="universityName">Название места обучения:</label>
                        <input class="form-control" type="text" id="universityName">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="universityDescription">Описание места обучения:</label>
                        <input class="form-control" type="text" id="universityDescription">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="specializationName">Название специальности:</label>
                        <input class="form-control" type="text" id="specializationName">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="specializationDescription">Описание специальности:</label>
                        <input class="form-control" type="text" id="specializationDescription">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="educationStart">Год/дата начала обучения:</label>
                        <input class="form-control" type="text" id="educationStart" placeholder="00.00.0000">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="educationEnd">Год/дата конца обучения:</label>
                        <input class="form-control" type="text" id="educationEnd" placeholder="00.00.0000">
                    </div>`
            }
            let closeButton = $(`<button type="button" class="btn-close close-form" aria-label="Close"></button>`)
            let createButton = $('<input class="btn btn-primary" type="submit" value="Создать">');
            let inputForm = $(`<div class="container edit-form"> <form id="createForm">`)
                .append(closeButton)
                .append(formfield)
                .append(createButton)
                .append(`</form> </div>`);

            createButton.click(function () {
                let createData = {};
                inputForm.find('input[class="form-control"]').each(function (key, value) {
                    createData[$(this).prop('id')] = $(this).val();
                });
                createData[$(inputForm.find('select[class="form-select"]')).prop('id')] = $(inputForm.find('select[class="form-select"]')).val()
                createData['agentId'] = $('#person_id').val();

                let targetEditUrl;
                if (theadData === 'products') {
                    targetEditUrl = processUrl + '/api/prices_by_agent/create'
                } else {
                    targetEditUrl = processUrl + '/api/education_by_agent/create'
                }

                if ($('#createForm').valid()) {
                    $('.alert').hide();
                    $.ajax({
                        url: targetEditUrl,
                        type: "POST",
                        dataType: "json",
                        headers: {
                            'X-CSRFToken': csrftoken,
                            'Authorization': 'Telegram ' + telegramId
                        },
                        traditional: true,
                        data: createData,
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

                inputForm.hide(100);
                $('.overlay').hide();
                inputForm.remove()
            });

            closeButton.click(function () {
                inputForm.hide(100)
                $('.overlay').hide();
                inputForm.remove()
            });

            // Добавление формы для создания в строку таблицы
            $('#main-div').append(inputForm);
            $('.overlay').show();
            $('.edit-form').show(100);
        })
    } else {
        loadClientInfo(telegramId, currentUrl, processUrl);
        let targetUrl = processUrl + '/api/orders_by_client/info?TelegramId=' + telegramId
        loadOrderInfo(targetUrl, statusArr);
    }

    if ($('#company_form').length) {
        loadCompanyInfo(telegramId, currentUrl, processUrl);
    }


    // SAVE INFO
    Telegram.WebApp.onEvent('mainButtonClicked', function () {
        // $(document).on('click','#save_info', function(){
        let validationPerson = $('#person_form').valid();

        let personId = $('#person_id').val();
        let personFio = $('#fio').val();
        let phoneNumber = $('#phone_number').val();
        let personDateBirth = $('#date_of_birth').val();
        let email = $('#email_username').val() + '@' + $('#email_server').val();
        if (email === '@') {
            email = '';
        }
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
            let commandWork = false;
            let contractWork = false;
            if ($('#command_work').attr('checked')) {
                commandWork = true;
            }
            if ($('#contract_work').attr('checked')) {
                contractWork = true;
            }
            additionalData = {
                'agent_description': $('#agent_description').val(),
                'education_description': $('#education_description').val(),
                'work_experience': $('#work_experience').val(),
                'command_work': commandWork,
                'contract_work': contractWork,
                'guarantee_period': $('#guarantee_period').val(),
            };
        } else {
            targetPersonUrl = processUrl + '/api/client/' + personId + '/';
            additionalData = {
                'address': $('#client_address').val(),
                'addition_information': $('#addition_information').val()
            };
        }

        if (validationPerson) {
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
            let companyName = $('#company_name').val();
            let legalAddress = $('#legal_address').val();
            let mailAddress = $('#mail_address').val();
            let emailAddress = $('#email_address').val();
            let contactPhone = $('#contact_phone').val();
            let inn = $('#inn').val();
            let kpp = $('#kpp').val();
            let ogrnip = $('#ogrnip').val();
            let paymentAccount = $('#payment_account').val();
            let bank = $('#bank').val();
            let bik = $('#bik').val();
            let okpo = $('#okpo').val();
            let description = $('#description').val();
            let targetCompanyUrl = processUrl + '/api/company/' + companyId + '/';

            if (validationCompany) {
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