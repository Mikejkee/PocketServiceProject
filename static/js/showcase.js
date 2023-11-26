window.Telegram.WebApp.ready();
let tg = window.Telegram.WebApp;
tg.MainButton.text = 'Отправить заявку';
// tg.MainButton.show();

let csrftoken = $.cookie('csrftoken');

function loadCompanysInfo(currentUrl, processUrl) {
    let targetUrl = processUrl + '/api/company/'
    let listData
    $.ajax({
        url: targetUrl,
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(data) {
            listData = data;
        }
     });
    let listDataReturn = {}
    $.each(listData,function(key,value) {
        listDataReturn[value.id] = value.name
    })
    return listDataReturn;
}

function openForm(agentId, agentTg) {
    tg.MainButton.show();
    let TelegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/showcase')[0];

    $('#agents_container').css('display', 'none');
    let orderForm = $('#orderForm').fadeIn('slow');

    loadClientInfo(TelegramId, currentUrl, processUrl)

    let listProducts = []
    $(`#${agentId}`).find('.order-info').each(function (){
        $('#agent_products_drop').append(
            `<option value="${this.id}" id="${agentTg}">${this.textContent}</option>`
        )
    })
}

function loadAgentsInfo(currentUrl, processUrl, companysInfo) {
    let targetUrl = processUrl + '/api/agent/'
    let targetPricesUrl = processUrl + '/api/prices_by_agent/info?AgentId='
    let targetEducationUrl = processUrl + '/api/education_by_agent/info?AgentId='
    let targetCommentUrl = processUrl + '/api/comments_by_agent/info?AgentId='

    $.get(targetUrl).done(function(answer) {
        let listData = answer;
        console.log(listData);

        let bodyDiv = $('#agents_card')
        $.each(listData,function(key,value) {
            let fio = value.person_fio;
            if (fio === null) {
                fio = ""
                fio = (value.surname === null) ? fio + "" : fio + ` ${value.surname}`;
                fio = (value.name === null) ? fio + ""  : fio + ` ${value.name}`;
                fio = (value.patronymic === null) ? fio + ""  : fio + ` ${value.patronymic}`;
            }

            let agentImg = value.background_image
            if (agentImg === null) {
                agentImg = srcNobodyImg
            }

            let companyName = companysInfo[value.company]
            if (companyName === undefined) {
                companyName = 'Самозанятый'
            }

            let passport = srcDone
            if (value.passport_check === null || value.passport_check === false) {
                passport = srcCancel
            }
            let guarantee = srcDone
            if (value.guarantee_period === null || value.guarantee_period === false) {
                guarantee = srcCancel
            }
            let contract = srcDone
            if (value.contract_work === null || value.contract_work === false) {
                contract = srcCancel
            }
            let command = srcDone
            if (value.command_work === null || value.command_work === false) {
                command = srcCancel
            }

            bodyDiv.append(
                    `<div class="card text-center border-warning mb-3">
                        <div class="card-body" style="padding: 5% 1% 5% 1%;">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">
                                        <img src="${agentImg}" class="my_icons">
                                    </div>
                                    <div class="col-7">
                                        <p class="fio"> ${fio} </p>
                                        <div class="container-fluid">
                                            <div class="row">
                                                <div class="col">
                                                    <p class="card-title company"> ${companyName} </p>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col">
                                                    <img src="${passport}" class="my_icons_sm">
                                                        <p class="card-title icons_text"> Паспорт </p>
                                                </div>
                                                <div class="col">
                                                    <img src="${guarantee}" class="my_icons_sm">
                                                        <p class="card-title icons_text"> Гарантия </p>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col">
                                                    <img src="${contract}" class="my_icons_sm">
                                                        <p class="card-title icons_text"> Договор </p>
                                                </div>
                                                <div class="col">
                                                    <img src="${command}" class="my_icons_sm">
                                                        <p class="card-title icons_text"> Команда </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    <div class="container">
                        <div class="row">
                            <div class="col-xs-1"></div>
                            <div class="col-xs-10">
                                <p class="card-text agent_description"> ${value.agent_description} </p>
                            </div>
                            <div class="col-xs-1"></div>
                        </div>
                        <div class="row table-agent-info" style="margin: 10px 0px 10px 0px;">
                            <div class="panel-body">
                                <div class="pull-right">
                                    <div class="btn-group-sm" role="group">
                                        <button type="button" table-target="agent_${value.id}_table" class="btn btn-secondary btn-filter table-agent-info" data-target="products">Услуги/цены</button>
                                        <button type="button" table-target="agent_${value.id}_table" class="btn btn-secondary btn-filter table-agent-info" data-target="education">Образование</button>
                                        <button type="button" table-target="agent_${value.id}_table" class="btn btn-secondary btn-filter table-agent-info" data-target="feedback">Отзывы</button>
                                    </div>
                                </div>
                            </div>

                            <table class="table table-sm table-hover align-middle" id="agent_${value.id}_table">
                                <thead class="" data-status="products" style="">
                                    <tr>
                                        <th class="col-xs-9 table-agent-info" scope="col">Тип услуги</th>
                                        <th class="col-xs-3 table-agent-info" scope="col"> Цена </th>
                                    </tr>
                                </thead>
                                <thead class="" data-status="education" style="display: none;">
                                    <tr>
                                        <th class="col-xs-4 table-agent-info" scope="col"> ВУЗ </th>
                                        <th class="col-xs-4 table-agent-info" scope="col"> Специальность </th>
                                        <th class="col-xs-2 table-agent-info" scope="col"> Дата окончания </th>
                                        <th class="col-xs-1 table-agent-info" scope="col"> Подтверждение </th>
                                    </tr>
                                </thead>
                                <thead class="" data-status="feedback" style="display: none;">
                                    <tr>
                                        <th class="col-xs-4 table-agent-info" scope="col"> Оценка/дата </th>
                                        <th class="col-xs-4 table-agent-info" scope="col"> Комментарий </th>
                                    </tr>
                                </thead>

                                <tbody class="table-agent-info table-agent-info" id="${value.id}"> </tbody>
                            </table>

                            <button type="button" class="btn btn-outline-success" onclick="openForm(${value.id}, ${value.telegram_id})">Оставить заявку</button>  
                        </div>
                    </div>
                </div>`)

            // Загрузка цен и услуг агента
            $.get(targetPricesUrl+value.id).done(function(answer) {
                let listPrices = JSON.parse(answer.data);
                console.log(listPrices);

                let table = $(`#${value.id}`)
                $.each(listPrices,function(typeProduct,products) {
                     table.append(
                            `<tr class="table-group-divide table-dark" data-status="products">
                                <td colspan="2">
                                    <p class="text-center table-lc-p" style="margin-bottom: 0px;"> ${typeProduct} </p>
                                </td>
                            </tr>`
                     );
                    $.each(products,function(type_info, price_info) {
                        table.append(
                            `<tr data-status="products">
                                <td>
                                    <p class="text-center table-lc-p order-info" style="margin-bottom: 0px;" id="${price_info[1]}"> ${type_info} </p>
                                </td>
                                <td>
                                    <p class="text-center table-lc-p" style="margin-bottom: 0px;" > ${price_info[0]}</p>
                                </td>
                            </tr>`
                        );
                    })
                })
            })

            // Загрузка образования агента
            $.get(targetEducationUrl+value.id).done(function(answer) {
                let listEducations = JSON.parse(answer.data);
                console.log(listEducations);

                let table = $(`#${value.id}`)
                $.each(listEducations,function(key, educationInfo) {
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
                        </tr>`
                    );
                })
            })

            // Загрузка комментариев
            $.get(targetCommentUrl+value.id).done(function(answer) {
                let listComments = JSON.parse(answer.data);
                console.log(listComments);

                let table = $(`#${value.id}`)
                $.each(listComments,function(key, commentInfo) {
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
                     $.each(commentInfo.images, function (key, img){
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

        })
/*            let $photo = $('#userPhoto');
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
            $('#guarantee_period').val(data.guarantee_period);*/

        }).fail(function(err) {
            console.log(err);
        });
}

$(document).ready(function(){
    let telegramId = $('#telegram_id').val();
    let currentUrl = window.location.href;
    let processUrl = currentUrl.split('/showcase')[0];
    let companysInfo = loadCompanysInfo(currentUrl, processUrl)

    loadAgentsInfo(currentUrl, processUrl, companysInfo);

    // Create order INFO
    // Telegram.WebApp.onEvent('mainButtonClicked', function() {
    $(document).on('click','#create_order', function() {
        let validationOrder = $('#order_form').valid();
        let targetOrderUrl = processUrl + '/api/orders_by_client/create'

        let clientFio = $('#fio').val();
        let phoneNumber = $('#phone_number').val();
        let email = $('#email_username').val() + '@' + $('#email_server').val();
        if (email === '@') {
            email = '';
        }
        let address = $('#client_address') .val();

        let product = $('#agent_products_drop')
        let productId = product.val();
        let productInfo =  product.find(`option[value='${productId}']`).text();
        let agentId = product.find(`option[value='${productId}']`).attr('id');

        let orderName = $('#order_name').val();
        let orderPrice = $('#order_price').val();
        let orderStart = $('#order_start').val();
        let orderEnd = $('#order_end').val();
        let orderDescription = $('#order_description').val();

        let orderData = {
                'ClientId': telegramId,
                'ClientFIO': clientFio,
                'ClientPhone': phoneNumber,
                'ClientEmail': email,
                'ClientAddress': address,
                'AgentTelegramId': agentId,
                'ProductId': productId,
                'ProductInfo': productInfo,
                'OrderName': orderName,
                'OrderPrice': orderPrice,
                'OrderStart': orderStart,
                'OrderEnd': orderEnd,
                'OrderInfo': orderDescription,
            }


        if(validationOrder) {
            $('.alert').hide();
            $.ajax({
                url: targetOrderUrl,
                type: "POST",
                dataType: "json",
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Authorization': 'Telegram ' + telegramId
                },
                traditional: true,
                data: orderData,
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
        })
    })
