$(document).ready(function () {

    $('#vars_names').prop("selectedIndex", -1)

    $("#vars_names").on("change", function (){
        let var_name = $('#vars_names').find(":selected").text();
        console.log(var_name);
        $("#program").val(vars[var_name]['program']);
        $("#p1").val(vars[var_name]['p1']);
        $("#p2").val(vars[var_name]['p2']);
        $("#p3").val(vars[var_name]['p3']);
        $("#p4").val(vars[var_name]['p4']);
        $("#p5").val(vars[var_name]['p5']);
        $("#p6").val(vars[var_name]['p6']);
        if (isdeletable[var_name] == true) {
            $("#delete").prop('disabled', false);
        }
        else {
            $("#delete").prop('disabled', true);
        }
    });
});