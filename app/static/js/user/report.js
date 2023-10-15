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
        dictDefaultMessage: 'Перетащите файл, либо нажмите для выбора файла',
        dictCancelUpload: '',
        dictRemoveFile: 'Убрать файл',
        dictMaxFilesExceeded: 'Вы можете загрузить только один файл.',
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
            });

            this.on("success", function() {
                window.location.replace(window.location.pathname);
            });

            this.on('error', function(file, msg){
                alert(msg);
                this.removeFile(file);
            });
        }
    }

    $('#send-file').on('click', function(){
        $('.dz-progress').show();
        var dropzone = Dropzone.forElement("#dropper");
        dropzone.processQueue();
    });

});