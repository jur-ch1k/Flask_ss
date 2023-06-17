$(document).ready(function () {
    function bind() {
        $('.table_row .user-name').on('click', function () {
            $('input', $(this).parent()).prop('checked', !($('input', $(this).parent()).prop('checked')));
            $('input', $(this).parent()).toggleClass('checked')
        });

        $('.table_row .select-input input').on('click', function () {
            $(this).toggleClass('checked');
        });


        $('.tabs .tab-inline').on('click', function () {
            $('.tabs .tab-inline').removeClass('active');
            $(this).addClass('active');
            $('.tabs-content').hide();
            if ($(this).hasClass('tab-new'))
                $('.tabs-content.tab-new').show();
            else
                $('.tabs-content.tab-' + $(this).text().trim()).show();
        });

        $('.tabs-content input').on('focus', function () {
            $('.has-error', $(this).parent()).hide();
            $('.users_out-group', $(this).parent()).show();
        });

        $('.tabs-content input').on('focusout', function () {
            $('.users_out-group', $(this).parent()).hide();
        });

        $('.tabs-content input').on('keyup', function () {
            let block = $(this).parent(),
                userName = $(this).val().trim().toLowerCase(),
                usersBlock = $('.users_out-group div', block);
            usersBlock.each(function () {
                if ($(this).text().trim().toLowerCase().indexOf(userName) == -1)
                    $(this).hide()
                else $(this).show()
            });
        });

        $('.users_out-group div').on('mousedown', function () {
            let block = $(this).parent().parent(),
                userName = $(this).text().trim();
            $('input.add-new', block).val(userName);
        });


    };

    let countTabs = 0;
    $(groups).each(function (indxGroup, itemGroup) {
        countTabs++;
    });
    if (parseInt($('.groups-block .tabs-content').css('min-width')) < countTabs * 100 + 30) {
        $('.groups-block .tabs-content').css('width', countTabs * 100 + 30 + 'px');
    }

    bind();
    $('.delete_users').on('click', function () {
        let block = $(this).parent().parent();
        let usersDelete = {
            'usersDelete': [],
            'method': 'delete_users',
            'groupName': block.attr('name')
        };
        $('.table_row .select-input.content input.checked', block).each(function () {
            let userName = $(this).parents('.table_row').children('.user-name').text();
            if (userName != 'ucmc2020ssRoot')
                usersDelete.usersDelete.push(userName);
        });
        if (usersDelete['usersDelete'].length)
            $.ajax({
                method: "POST",
                contentType: "application/json; charset=utf-8",
                url: "/admin/groups_edit",
                data: JSON.stringify(usersDelete),
                dataType: "json",
                success: (data) => {
                    let groupName = block.attr('name')
                    $('.table_row .user-name', block).each(function () {
                        if (usersDelete['usersDelete'].indexOf($('p', this).text().trim()) != -1) {
                            let login = $('p', this).text().trim();
                            $(this).parent().remove();
                            $(groups).each(function (indxGroup, itemGroup) {
                                if (itemGroup['name'] == groupName) {
                                    let index = groups[indxGroup]['users'].indexOf(login);
                                    groups[indxGroup]['users'].splice(index, 1);
                                }
                            });
                        }
                    });
                    // window.location.replace(window.location.pathname);
                },
                error: (data) => {
                    console.log('request error')
                }
            });
    });

    $('.add_users').on('click', function () {
        let block = $(this).parent().parent(),
            input = $('input.add-new', block),
            inputName = input.val().trim(),
            userExist = false;
        if (inputName) {
            $(users).each(function (indx, item) {
                if (item == inputName)
                    userExist = true;
            });
            if (!userExist) {
                $('.has-error', block).text('*Логин не существует');
                $('.has-error', block).show();
                input.val('');
            } else {
                let newUser = {'newUser': inputName, 'method': 'add_user', 'groupName': block.attr('name')};
                $.ajax({
                    method: "POST",
                    contentType: "application/json; charset=utf-8",
                    url: "/admin/groups_edit",
                    data: JSON.stringify(newUser),
                    dataType: "json",
                    success: (data) => {
                        let newRow = $('<div class="table_row\"><span class=\"select-input content\"><input type=\"checkbox\"></span><span class=\"user-name\"><p>' + inputName + '</p></span></div>')
                        $('.users-table', block).append(newRow);
                        $(groups).each(function (indxGroup, itemGroup) {
                            if (itemGroup['name'] == block.attr('name'))
                                groups[indxGroup]['users'].push(inputName);
                        });
                        $('.users_out-group div', block).each(function () {
                            if ($(this).text().trim() == inputName)
                                $(this).remove();
                        });
                        input.val('');
                        bind();
                    },
                    error: (data) => {
                        console.log('request error')
                    }
                });
            }
        } else {
            $('.has-error', block).text('*Логин не может принимать пустое значение');
            $('.has-error', block).show();
        }
    });

    $('.delete_group').on('click', function () {
        let block = $(this).parent().parent();
        let group = {'method': 'delete_group', 'groupName': block.attr('name')};
        $.ajax({
            method: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/admin/groups_edit",
            data: JSON.stringify(group),
            dataType: "json",
            success: (data) => {
                window.location.replace(window.location.pathname);
            },
            error: (data) => {
                console.log('request error')
            }
        });
    });

    $('#add_group').on('click', function () {
        let block = $(this).parent().parent(),
            input = $('input', block),
            inputName = input.val().trim(),
            groupExist = false;
        if (inputName) {
            $(groups).each(function (indx, item) {
                if (item['name'] == inputName)
                    groupExist = true;
            });
            if (groupExist) {
                $('.has-error', block).text('*Группа с таким названием уже существует');
                $('.has-error', block).show();
                input.val('');
            } else {
                let newGroup = {'newGroup': inputName, 'method': 'add_group'};
                $.ajax({
                    method: "POST",
                    contentType: "application/json; charset=utf-8",
                    url: "/admin/groups_edit",
                    data: JSON.stringify(newGroup),
                    dataType: "json",
                    success: (data) => {
                        window.location.replace(window.location.pathname);
                    },
                    error: (data) => {
                        console.log('request error')
                    }
                });
            }
        } else {
            $('.has-error', block).text('*Имя группы не может принимать пустое значение');
            $('.has-error', block).show();
        }
    });

});