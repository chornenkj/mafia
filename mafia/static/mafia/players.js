/* AJAX script to load add player form */
var href = $("#add_player_name").attr('href');
function load_add_player() {
$.ajax({
    type: 'GET',
    async: true,
    url: href,
    dataType: 'html',
    success: function(response, statusText, xhr){
        var redirect = null;
        try {
            redirect = $.parseJSON(xhr.responseText).redirect;
            window.location.href = redirect.replace(/\?.*$/, "?next=" + window.location.pathname);
        } catch (e) {
            $("#add_player_name").html(response);
        };
    }
});
};
$(document).ready(function () {
    load_add_player();
    setTimeout(function(){ $("#id_title").focus(); }, 100);
});