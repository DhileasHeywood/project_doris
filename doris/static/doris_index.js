$( document ).ready(function (){
$.ajax({
    url: "/application/entry_update", data: JSON.stringify(update_object), dataType: "json", contentType:
        "application/json", method: "POST", success:
});

});