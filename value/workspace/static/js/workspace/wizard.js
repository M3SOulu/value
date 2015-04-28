$(function () {

  var FORWARD = 1;
  var BACKWARD = -1;
  var ENTER_KEY = 13;

  var wizard_steps = ["#basic-data", "#stakeholders", "#decision-making"];
  var current_step_index = 0;

  var wizard_integrity_control = function () {
    if (current_step_index == 0) {
      $(".js-previous-wizard-step").prop("disabled", true);
    }
    else {
      $(".js-previous-wizard-step").prop("disabled", false);
    }

    if (current_step_index == 2) {
      $(".js-submit-wizard").show();
      $(".js-next-wizard-step").hide();
    }
    else {
      $(".js-submit-wizard").hide();
      $(".js-next-wizard-step").show();
    }

  };

  var display_content = function (direction) {
    var last_step;
    var current_step;

    last_step = wizard_steps[current_step_index];
    current_step_index = current_step_index + direction;
    current_step = wizard_steps[current_step_index];

    $(".wizard-content section:visible").fadeOut(400, function () {
      $(".wizard-content section" + current_step).fadeIn(400);
      if (direction == FORWARD) {
        $(".js-wizard-steps button[data-target='" + last_step + "'] .glyphicon").show();
        $(".js-wizard-steps button[data-target='" + current_step + "']").removeClass("btn-default").addClass("btn-primary").prop("disabled", false);
      }
      else if (direction == BACKWARD) {
        $(".js-wizard-steps button[data-target='" + current_step + "'] .glyphicon").hide();
        $(".js-wizard-steps button[data-target='" + last_step + "']").removeClass("btn-primary").addClass("btn-default").prop("disabled", true);
      }
      wizard_integrity_control();
    });
  };

  $(".js-wizard-steps button").click(function () {
    var target;
    target = $(this).attr("data-target");

    if ("#" + $(".wizard-content section:visible").attr("id") == target) {
      return false;
    }

  });

  $(".js-next-wizard-step").click(function () {
    if (current_step_index == 0) {
      if ($("#id_name").val() === "") {
        $("#id_name").closest(".form-group").addClass("has-error");
        $("#id_name").siblings(".help-block").show();
        return false;
      }
      else {
        $("#id_name").closest(".form-group").removeClass("has-error");
        $("#id_name").siblings(".help-block").hide();
      }
    }
    display_content(FORWARD);
  });

  $(".js-previous-wizard-step").click(function () {
    display_content(BACKWARD);
  });


  $(".js-stakeholder-selection").click(function () {

    if ($(this).hasClass("bg-success")) {
      $(this).removeClass("bg-success");
      $(".glyphicon-ok", this).hide();
      $("[name='stakeholders']", this).prop("checked", false);
    }

    else {
      $(this).addClass("bg-success");
      $(".glyphicon-ok", this).show();
      $("[name='stakeholders']", this).prop("checked", true);
    }

  });

  $(".js-stakeholders-select-all").click(function () {
    $(".js-stakeholder-selection").each(function () {
      $(this).addClass("bg-success");
      $(".glyphicon-ok", this).show();
      $("[name='stakeholders']", this).prop("checked", true);
    });
  });

  $(".js-stakeholders-select-none").click(function () {
    $(".js-stakeholder-selection").each(function () {
      $(this).removeClass("bg-success");
      $(".glyphicon-ok", this).hide();
      $("[name='stakeholders']", this).prop("checked", false);
    });
  });

  $(".js-multiple-items").click(function () {

    if ($(this).val() === "yes") {
      $(".instance-items").show();
      $(".js-add-item").focus();
    }
    else {
      $(".instance-items").hide();
    }

  });

  var add_item = function (value) {

    if (value.length > 0) {
      var template = [
        "<li class='list-group-item'>",
        "<a href='javascript:void(0);' class='pull-right'><span class='glyphicon glyphicon-remove-sign js-remove-item'></span></a>",
        "<input type='hidden' name='instance_item' value='{value}'>",
        "{value}",
        "</li>"
        ];
      var html = template.join("\n").replace(/{value}/g, value);
      $(".instance-items .list-group").prepend(html);
      $(".js-add-item").val("");
    }

  };

  $(".js-add-item").keydown(function (evt) {

    var key_code = evt.which?evt.which:evt.keyCode;

    if (key_code == ENTER_KEY) {
      var value = $(this).val();
      var list = [];

      if (value.indexOf(",") !== -1) {
        list = value.split(",");
      }

      else if (value.indexOf(";") !== -1) {
        list = value.split(";");
      }

      if (list.length > 0) {
        list.forEach(function (e) {
          add_item(e);
        });
      }

      else {
        add_item(value);
      }

      return false;
    }

  });

  $(".js-add-item").keyup(function (evt) {

    var data = $(".js-add-item").val();
    var match = /\r|\n/.exec(data);
    if (match) {
      var list = data.split("\n");
      list.forEach(function (e) {
        add_item(e);
      });
    }

  });

  $(".js-btn-add-item").click(function () {
    var value = $(".js-add-item").val();
    var list = [];

    if (value.indexOf(",") !== -1) {
      list = value.split(",");
    }

    else if (value.indexOf(";") !== -1) {
      list = value.split(";");
    }

    if (list.length > 0) {
      list.forEach(function (e) {
        add_item(e);
      });
    }

    else {
      add_item(value);
    }
  });


  $(".list-group").on("click", ".js-remove-item", function () {
    $(this).closest("li").remove();
  });

  $(".js-submit-wizard").click(function () {
    $(".js-wizard-steps button[data-target='#decision-making'] .glyphicon").show();
  });
  
});