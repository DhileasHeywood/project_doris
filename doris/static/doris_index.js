$( document ).ready(function (){
    $("#bid_search").select2({
        maximumSelectionLength: 1
    });
});

$("#search_bid").click(function (){

    let bid_title =  $("#bid_search").select2("data")[0]["text"]

    $.ajax({
    url: "/application/", data: JSON.stringify(bid_title), dataType: "json", contentType:
        "application/json", method: "POST", success:
            function (result){
                if (result === 200) {



                } else {
                    alert("can't find the bid!");
                }
            }, error: function (){
            console.log("Nothing is happening");
    }

    })
})