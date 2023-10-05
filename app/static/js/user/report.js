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

    Dropzone.options.dropper = {
        paramName: 'file',
        chunking: true,
        forceChunking: true,
        url: '/upload_report',
        chunkSize: 1000000,
        autoProcessQueue: false,
        maxFiles: 1,
        addRemoveLinks: true,
        createImageThumbnails: false,
        init: function() {

            this.on("addedfile", function(file) {
                $('.dz-progress').hide();
                if (this.files.length > 1) {
                    alert("Вы можете загрузить только один файл.");
                    this.removeFile(file);
                }
            });

            this.on("success", function() {
                window.location.replace(window.location.pathname);
            });

            this.on('error', function(e){
                //alert(e);
            });
        }
    }

    $('#send-file').on('click', function(){
        $('.dz-progress').show();
        var dropzone = Dropzone.forElement("#dropper");
        dropzone.processQueue();
    });

});