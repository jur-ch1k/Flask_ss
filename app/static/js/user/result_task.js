$(document).ready(function () {
    let str = $('#xml_code').text().split("\n");
    $('#xml_code').text("");
    $(str).each(function (indx, item) {
        // console.log($("#xml_code").text());
        // нахождение тегов и запись их в классы для дальнейшей стилизации текста
        let indxBegin = item.indexOf('<'),
            indxEnd = (item.indexOf('>', indxBegin) < item.indexOf(' ', indxBegin)
                || item.indexOf(' ', indxBegin) == -1) ?
                item.indexOf('>', indxBegin) : item.indexOf(' ', indxBegin),
            classStr = item.substr(indxBegin + 1, indxEnd - indxBegin - 1);
        // сведение слассов типа "class" и "/class" к одному типу "class"
        if (classStr.indexOf('/') != -1)
            classStr = classStr.substr(classStr.indexOf('/') + 1, classStr.length - 1);
        let elemText = item.substr(item.indexOf(classStr) + classStr.length, item.length),
            openTeg = '<' + classStr,
            closeTeg;
        if (elemText.indexOf(classStr) != -1) {
            elemText = elemText.substr(0, elemText.indexOf(classStr) - 3);
            closeTeg = "></" + classStr + '>';
        } else {
            elemText = elemText.substr(0, elemText.indexOf('>'));
            closeTeg = '>';
        }
        console.log(elemText);
        // добавение нового элемента в блок кода
        let elem = $("<p><span class='string_index'>" + indx + "</span></p>");
        // elem.append(<span></span>)
        if (classStr.length > 0) {
            elem.append($("<span class='teg' style='padding-left: " + (indxBegin * 40 + 20) + "px'></span>").text(openTeg));
            elem.append($("<span>" + elemText + "</span>"));
            elem.append($("<span class='teg'></span>").text(closeTeg));
        }
        $('#xml_code').append(elem);

    })

    $('#xml_code-button').on('click', function () {
        if ($('#xml_code').is(':hidden')) {
            $('#xml_code').slideDown("slow");
            $('img',this).css("transform", "rotate(180deg)");
        }
        else {
            $('#xml_code').slideUp("slow");
            $('img', this).css("transform", "rotate(0deg)");
        }
    });
});