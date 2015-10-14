$(function () {
  $(document).on("click", ".js-decision-item-details", function () {
    $(this).tooltip("hide");
    var url = $(this).attr("data-remote-url");
    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        $("#modal-decision-item-details .modal-body").html("");
      },
      success: function (data) {
        $("#modal-decision-item-details .modal-body").html(data);
      }
    });
  });

  $(".js-change-meeting-status").click(function () {
    var option = $(this).attr("data-option");
    $("#meeting-status").val(option);
    if (option === "C") {
      $("#close-meeting").modal("show");
    }
    else {
      $("#form-meeting-status").submit();
    }
  });

  $("#confirm-close-meeting").click(function () {
    $("#form-meeting-status").submit();
  });

  $(".js-meeting-notes").click(function () {
    var url = $(this).attr("data-remote-url");
    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        $("#modal-meeting-notes .modal-body").html("");
      },
      success: function (data) {
        $("#modal-meeting-notes .modal-body").html(data);
      }
    });
  });

  var updateMeetingProgress = function () {
    var url = $("#meeting-progress").attr("data-remote-url");
    var status = $("#meeting-progress").attr("data-meeting-status");
    if (status !== "C") {
      $.ajax({
        url: url,
        cache: false,
        dataType: 'json',
        success: function (data) {
          if (data.meeting_closed) {
            location.reload();
          }
          else {
            $("#meeting-progress").replaceWith(data.html);
          }
        },
        complete: function () {
          window.setTimeout(updateMeetingProgress, 10000);
        }
      });
    }
  };
  updateMeetingProgress();

});
