$(document).ready(function () {
    $('.table_row .report-name').each(function () {
        let width = $(this).innerWidth(),
            pWidth = $('a', this).innerWidth();
        let symbolWidth = Math.floor(pWidth / $('a', this).text().length) + 1;
        if (pWidth > width) {
            $('a', this).text(($('a', this).text()).substr(0, Math.floor(width / symbolWidth) - 3) + '...');
        }
    });
    $('.table_row .report-mark').each(function () {
        if ($('input', this).val() == 'None')
            $('input', this).val('');
    });
    $('.table_row .report-comment').each(function () {
        if ($('input', this).val() == 'None')
            $('input', this).val('');
    });
    $('.table-header .select-input input').on('click', function () {
        let choice = $(this).prop('checked');
        $('.table-content .select-input.content input').each(function () {
            $(this).prop('checked', choice);
            if (choice)
                $(this).addClass('checked')
            else $(this).removeClass('checked');
        })
    });
    $('.table-content .select-input.content input').on('click', function () {
        $(this).toggleClass('checked');
    })
    $('.edit-block #delete_users').on('click', function () {
        let reportsDelete = {'reportsDelete': [], 'method': 'delete_reports'};
        $('.table-content .select-input.content input.checked').each(function () {
            let userName = $(this).parents('.table_row').children('.report-user').text().trim();
            let reportName = $(this).parents('.table_row').children('.report-name').children('a').attr('data');
            console.log(reportName);
            reportsDelete['reportsDelete'].push({'user': userName, 'report': reportName});
        });
        // console.log(reportsDelete)
        // console.log(JSON.stringify(usersDelete.data));
        $.ajax({
            method: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/admin/reports",
            data: JSON.stringify(reportsDelete),
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
    $('.table-header span.filter').on('click', function () {
        $('.table-header span').removeClass('active');
        $(this).addClass('active');
        let filter = $(this).attr('filter-data');
        $('.table-content').sort(function (a, b) {
            let textA = $('span.' + filter, a).text().trim(),
                textB = $('span.' + filter, b).text().trim();
            if (filter == 'report-mark') {
                textA = parseInt($('span.' + filter + ' input', a).val())
                textB = parseInt($('span.' + filter + ' input', b).val())
                if (!textA)
                    textA = 0;
                if (!textB)
                    textB = 0;
            }
            // console.log(textA>textB?textA:textB);
            return textA < textB ? -1 : 1;
        }).appendTo($('.table-content').parent());
        ;
    });
    $('.table-content span.report-mark input').on('keyup', function () {
        let mark = parseInt($(this).val());
        if (mark)
            $(this).val(mark);
        else
            $(this).val('');
    });
    $('.table-content span.report-mark input').on('focusout', function () {
        let element = $(this).parent().parent().parent();
        let reportEdit = {'user': '', 'report': '', 'method': 'edit_mark', 'mark': 0};
        reportEdit['mark'] = parseInt($(this).val())
        if (reportEdit['mark']) {
            reportEdit['user'] = element.children('.report-user').text().trim();
            reportEdit['report'] = element.children('.report-name').children('a').attr('data');
            // console.log(JSON.stringify(usersDelete.data));
            console.log(reportEdit)
            $.ajax({
                method: "POST",
                contentType: "application/json; charset=utf-8",
                url: "/admin/reports",
                data: JSON.stringify(reportEdit),
                dataType: "json",
                success: (data) => {
                    // console.log('isChat response: ' + data)
                    // window.location.replace(window.location.pathname);
                },
                error: (data) => {
                    console.log('request error')
                }
            });
        }
    });
    $('.table-content span.report-comment input').on('focusout', function () {
        let element = $(this).parent().parent().parent();
        let reportEdit = {'user': '', 'report': '', 'method': 'edit_comment', 'comment': ''};
        reportEdit['comment'] = $(this).val()
        reportEdit['user'] = element.children('.report-user').text().trim();
        reportEdit['report'] = element.children('.report-name').children('a').attr('data');
        // console.log(JSON.stringify(usersDelete.data));
        console.log(reportEdit)
        $.ajax({
            method: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/admin/reports",
            data: JSON.stringify(reportEdit),
            dataType: "json",
            success: (data) => {
                // console.log('isChat response: ' + data)
                // window.location.replace(window.location.pathname);
            },
            error: (data) => {
                console.log('request error')
            }
        });
    });
});