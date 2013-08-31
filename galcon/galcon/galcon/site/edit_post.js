function wrap_text(elementID, openTag, closeTag) {
    var textArea = $('#' + elementID);
    var len = textArea.val().length;
    var start = textArea[0].selectionStart;
    var end = textArea[0].selectionEnd;
    var selectedText = textArea.val().substring(start, end);
    var replacement = openTag + selectedText + closeTag;
    textArea.val(textArea.val().substring(0, start) + replacement + textArea.val().substring(end, len));
}

function insert_at_cursor(element_id, text) {
    var element = document.getElementById(element_id);
    if (document.selection) {
        element.focus();
        var sel = document.selection.createRange();
        sel.text = text;
        element.focus();
    } else if (element.selectionStart || element.selectionStart === 0) {
        var startPos = element.selectionStart;
        var endPos = element.selectionEnd;
        var scrollTop = element.scrollTop;
        element.value = element.value.substring(0, startPos) + text + element.value.substring(endPos, element.value.length);
        element.focus();
        element.selectionStart = startPos + text.length;
        element.selectionEnd = startPos + text.length;
        element.scrollTop = scrollTop;
    } else {
        element.value += text;
        element.focus();
    }
}

function make_bold() {
    wrap_text("text", "<b>", "</b>");
}   

function make_italicized() {
    wrap_text("text", "<i>", "</i>");
}

function make_underlined() {
    wrap_text("text", "<u>", "</u>");
}

function make_quoted() {
    wrap_text("text", "<blockquote>", "</blockquote>");
}

function insert_image() {
    insert_at_cursor("text", '<img src=""/>');
}
