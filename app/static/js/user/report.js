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
        if ($('p', this).text() == 'None')
            $('p', this).text('');
    });
    $('.table_row .report-comment').each(function () {
        if ($('p', this).text() == 'None')
            $('p', this).text('');
    });
    $('.table_row .teacher_name').each(function () {
        if ($('p', this).text() == 'None')
            $('p', this).text('');
    });
    $('.table_row .report-name p').on('click', function () {

    });
});