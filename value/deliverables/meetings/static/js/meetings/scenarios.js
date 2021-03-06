$(function () {

    /* Scenario details functions */

    $(document).on("click", ".js-scenario-details", function () {
        var $btn = $(this);
        $.ajax({
            url: $btn.data("remote-url"),
            beforeSend: function () {
                $("#modal-scenario-details .modal-body").loading();
            },
            success: function (data) {
                $("#modal-scenario-details .modal-body").html(data);
            }
        });
    });

    /* Add scenario functions */

    $(document).on("click", ".js-scenario-add", function () {
        $("#add-next").val($(this).attr("data-next"));
    });

    $("#modal-add-scenario").on("shown.bs.modal", function () {
        $.ajax({
            url: $("#form-add-scenario").attr("action"),
            dataType: 'json',
            beforeSend: function () {
                $("#modal-add-scenario .modal-body").loading();
            },
            success: function (data) {
                var DESCENDING = 1;
                var VALUE_RANKING_COLUMN = 3;

                $("#modal-add-scenario .modal-body").html(data.form);
                $("#add-table-decision-items").tablesorter({
                    headers: {0: {sorter: false}},
                    sortList: [[VALUE_RANKING_COLUMN, DESCENDING]]
                });
                initializeCheckAll();
                var initial_selection = $("#form-add-scenario").data("initial-selection");
                if (initial_selection !== undefined) {
                    var ids = initial_selection.split(' ');
                    ids.forEach(function (meeting_item_id) {
                        var $input = $("#add-table-decision-items input[name='add-meeting_items'][value='" + meeting_item_id + "']")
                        $input.prop("checked", true);
                        $("#add-table-decision-items tbody").prepend($input.closest("tr"));
                    });
                }
            },
            complete: function () {
                $("#modal-add-scenario .modal-body").loading();
            }
        });
    });
    $("#modal-add-scenario").on("hidden.bs.modal", function () {
        $("#modal-add-scenario .modal-body").html("");
        $("#form-add-scenario").data("initial-selection", "");
    });

    $("#form-add-scenario").submit(function () {
        $.ajax({
            url: $("#form-add-scenario").attr("action"),
            data: $("#form-add-scenario").serialize(),
            type: $("#form-add-scenario").attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.is_valid) {
                    if ("redirect_to" in data) {
                        location.href = data["redirect_to"];
                    }
                    $.get("", function (data) {
                        $("#scenarios").replaceWith($("#scenarios", data));
                        $("#scenarios-menu").replaceWith($("#scenarios-menu", data));
                        $(".charts [data-preload='True']").each(function () {
                            $(".panel-heading", this).loadchart();
                        });
                    }, "html");
                    $("#modal-add-scenario").modal("hide");
                } else {
                    $("#modal-add-scenario .modal-body").html(data.form);
                    $("#add-table-decision-items").tablesorter({headers: {0: {sorter: false}}});
                    initializeCheckAll();
                }
            }
        });
        return false;
    });

    /* Edit scenario functions */

    $(document).on("click", ".btn-chart-edit", function () {
        var url = $(this).attr("data-remote-url");
        $("#form-edit-scenario").attr("action", url);
    });

    $("#modal-edit-scenario").on("shown.bs.modal", function () {
        $.ajax({
            url: $("#form-edit-scenario").attr("action"),
            dataType: 'json',
            beforeSend: function () {
                $("#modal-edit-scenario .modal-body").loading();
            },
            success: function (data) {
                var DESCENDING = 1;
                var VALUE_RANKING_COLUMN = 3;

                $("#modal-edit-scenario .modal-body").html(data.form);
                $("#edit-table-decision-items").tablesorter({
                    headers: {0: {sorter: false}},
                    sortList: [[VALUE_RANKING_COLUMN, DESCENDING]]
                });
                initializeCheckAll();
            },
            complete: function () {
                $("#modal-edit-scenario .modal-body").loading();
            }
        });
    });
    $("#modal-edit-scenario").on("hidden.bs.modal", function () {
        $("#modal-edit-scenario .modal-body").html("");
    });

    $("#form-edit-scenario").submit(function () {
        $.ajax({
            url: $("#form-edit-scenario").attr("action"),
            data: $("#form-edit-scenario").serialize(),
            type: $("#form-edit-scenario").attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.is_valid) {
                    $.get("", function (data) {
                        $("#scenarios").replaceWith($("#scenarios", data));
                        $("#scenarios-menu").replaceWith($("#scenarios-menu", data));
                        $(".charts [data-preload='True']").each(function () {
                            $(".panel-heading", this).loadchart();
                        });
                    }, "html");
                    $("#modal-edit-scenario").modal("hide");
                } else {
                    $("#modal-edit-scenario .modal-body").html(data.form);
                    $("#edit-table-decision-items").tablesorter({headers: {0: {sorter: false}}});
                    initializeCheckAll();
                }
            }
        });
        return false;
    });

    /* Scenario builder functions */

    $(document).on("click", ".js-scenario-builder", function () {
        $("#build-next").val($(this).attr("data-next"));
    });

    $("#modal-scenario-builder").on("shown.bs.modal", function () {
        var url = $(".js-scenario-builder").attr("data-remote-url");
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#modal-scenario-builder .modal-body").loading();
            },
            success: function (data) {
                $("#modal-scenario-builder .modal-body").html(data.form);
            },
            complete: function () {
                $("#modal-scenario-builder .modal-body").loading();
            }
        });
    });
    $("#modal-scenario-builder").on("hidden.bs.modal", function () {
        $("#modal-scenario-builder .modal-body").html("");
    });

    $("#form-scenario-builder").submit(function () {
        var form = $(this);
        $.ajax({
            url: $(form).attr("action"),
            type: $(form).attr("method"),
            data: $(form).serialize(),
            success: function (data) {
                if (data.is_valid) {
                    if ("redirect_to" in data) {
                        location.href = data["redirect_to"];
                    }
                    $.get("", function (data) {
                        $("#scenarios").replaceWith($("#scenarios", data));
                        $("#scenarios-menu").replaceWith($("#scenarios-menu", data));
                        $("#scenarios .panel-heading:eq(0)").loadchart();
                    }, "html");
                    $("#modal-scenario-builder").modal("hide");
                } else {
                    $("#modal-scenario-builder .modal-body").html(data.form);
                }
            }
        });
        return false;
    });

    /* Scenario compare functions */

    $(".js-scenario-compare").click(function () {
        var url = $("#form-scenario-compare").attr("action");
        $.get(url, function (data) {
            $("#modal-scenario-compare .modal-dialog").html(data.form);
        }, "json");
    });

    $("#form-scenario-compare").submit(function () {
        var form = $(this);
        $.ajax({
            url: $(form).attr("action"),
            type: $(form).attr("method"),
            data: $(form).serialize(),
            cache: false,
            success: function (data) {
                if (data.is_valid) {
                    $("#modal-scenario-compare").modal("hide");
                    $("#expand-chart .modal-title").text("Scenarios comparison");
                    $("#expand-chart .modal-body").html("");
                    setTimeout(function () {
                        $("#expand-chart").modal("show");
                        setTimeout(function () {
                            $("#expand-chart .modal-body").html(data.html);
                            $("#expand-chart .btn-chart-expand, #expand-chart .btn-chart-info").remove();
                            $("#expand-chart [data-preload='True']").each(function () {
                                $(".panel-heading", this).loadchart();
                            });
                        }, 250);
                    }, 500)
                } else {
                    $("#modal-scenario-compare .modal-dialog").html(data.form);
                }
            }
        });
        return false;
    });

});
