function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}/`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.task_id}</td>
        <td>${res.task_status}</td>
        <td>${res.task_result}</td>
      </tr>`
    $('#controllers').prepend(html);

    const taskStatus = res.task_status;

    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}

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


$(document).on('click', '.form-check-input',function() {
    if ($(this).is(':checked') === true) {
        $(this).attr('checked', '');
    }
    else {
        $(this).removeAttr('checked');
    }
});

$(document).on('click', '.btn-filter', function () {
    let target = $(this).data('target');
    let table = $(this).attr('table-target');

    if (target === 'feedback') {
        $('#createInfo').css('display', 'none')
    }
    else {
        $('#createInfo').css('display', '')
    }

    $(`#${table} thead`).css('display', 'none');
    $(`#${table} tr[data-status]`).css('display', 'none');
    $(`#${table} tr[data-status="${target}"]`).fadeIn('slow');
    $(`#${table} thead[data-status="${target}"]`).fadeIn('slow');


    $('[data-fancybox]').fancybox({
      protect: true,
      clickContent : function(current, event) {
          return current.type === 'image' ? 'close' : 'zoom';
      },
      mobile: {
          preventCaptionOverlap: !1,
          idleTime: !1,
          clickContent: function (current, event) {
              return "image" === current.type && "close";
          },
          clickSlide: function (current, event) {
              return "image" === current.type && "close";
          },
      }
    });
});
