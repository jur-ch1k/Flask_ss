$(document).ready(function () {
    // console.log("skrf");
    $('.table_row .select-input.content input').on('click', function () {
        $(this).toggleClass('checked');
    });
    $('.edit-block #mask_for_select').on('focus keyup focusout', function () {
        if ($(this).val().length > 0)
            $('.edit-block label').hide();
        else
            $('.edit-block label').show();
    });
    $('#select_by_mask').on('click',function (){
        let mask = $('.edit-block #mask_for_select').val().replace(/[^a-zA-Z0-9]/gi, '');
        $('.edit-block #mask_for_select').val(mask);
        $('.users-table .table_row .select-input input').removeClass('checked');
        $('.users-table .table_row .select-input input').prop('checked',false);
       $('.users-table .table_row').each(function (){
            if($('.user-name p',this).text().indexOf(mask)+1) {
                $('.select-input input', this).addClass('checked');
                $('.select-input input', this).prop('checked',true);
            }
       });
    });
    $('.edit-block #delete_users').on('click', function () {
        let usersDelete = {'usersDelete': []};
        $('.table_row .select-input.content input.checked').each(function () {
            let userName = $(this).parents('.table_row').children('.user-name').text();
            if (userName != 'ucmc2020ssRoot')
                usersDelete.usersDelete.push(userName);
        });
        // console.log(JSON.stringify(usersDelete.data));
        $.ajax({
            method: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/admin/users",
            data: JSON.stringify(usersDelete),
            dataType: "json",
            success: (data) => {
                // console.log('isChat response: ' + data)
                window.location.replace(window.location.pathname);
            },
            error: (data) => {
                console.log('request error')
            }
        });
    });
});