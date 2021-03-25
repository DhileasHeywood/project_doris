$("#tags_clicked").select2({
    tags: true
})
$("#project_tags_clicked").select2({
    tags: true
})

$('#search_entries_btn').click(function(){

     // define query object - a dictionary
let query_object = { "query": {   }}
// if tags and/or project tags checked: query object = { query: { term: { tags: "text", project_tags:
// "text" }}}
let tagsCheckbox = $('#search_tags_check');
let projTagsCheckbox = $('#search_proj_tags_check');
let bodyCheckbox = $('#search_body_check');
let searchText = $('#search_entries').val();


if (tagsCheckbox.prop("checked") && projTagsCheckbox.prop("checked")){
    query_object = {"query":{"bool":{"should":[{ "term": {"tags": searchText}}, { "term": { "project_tags":
                        searchText}}]}}};
    console.log(JSON.stringify(query_object));
} else if (tagsCheckbox.prop("checked")){
    query_object = {"query":{"term":{"tags":searchText}}};
    console.log(JSON.stringify(query_object));
} else if (projTagsCheckbox.prop("checked")){
    query_object = {"query":{"term":{"project_tags":searchText}}};
    console.log(JSON.stringify(query_object));
} else if (bodyCheckbox.prop("checked")) {
    query_object = {"query": {"match": {"body": searchText}}};
    console.log(JSON.stringify((query_object)));
}
// if body checked: query object =
// $.ajax({url: "/application/entry_search", data: "query object", type: "POST", success: function(result){
//      $('#search_results').html(result);
//      }

$.ajax({url: "/application/entry_search", data: JSON.stringify(query_object), dataType: "json", contentType:
        "application/json",
    method:"POST", success:
    function(result){
    console.log(result);
    let result_array = []
    for (let res of result)
        //this only works when tags and project_tags are lists.
        result_array.push('<div class="bg-white doris-sr border border-dark m-2 pl-1"' +
            ' onmouseover="highlightResult(this)" onmouseout="unhighlightResult(this)"' +
            ' onclick="getClickResult(this)">Tags: ' + res[0]['tags'].join(", ") +
            '<br>Project ' + 'Tags: ' + res[0]['project_tags'].join(", ") + '<br>Body: ' + res[0]['body'] +
            '<br>Date: ' + res[0]['date'] + '</div>');


    // Currently if there's an error, the previous results will display in the search_results window. I want to make
        // it so that that will clear to make it more user friendly.
    $('#search_results').html(result_array);




      }, error: function (){
      alert("Nothing is happening");
      } });
});

let clicked_id = 0
let clicked_proj_tags = []
let clicked_tags = []
let clicked_body = []

function getClickResult(x) {
    //retrieve body of clicked result
    let x_text = x.innerHTML.split('<br>');
    let x_body = x_text[2].split(': ')[1]

    // retrieve document from elasticsearch
    query_object = {"query": {"match": {"body": JSON.stringify(x_body)}}}

    $.ajax({
        url: "/application/entry_search", data: JSON.stringify(query_object), dataType: "json", contentType:
            "application/json",
        method: "POST", success:
            function (result) {
                // take first result (body search finds all sorts of things, and since the first will be an exact
                // match every time, I'm comfortable just taking that)
                let res = result[0]

                // store result in global object so that it's accessible for other implementation. Don't want to
                // read HTML because that's SUPER dodgy. Could lead to all sorts of issues. Don't do that.

                clicked_proj_tags = res[0]['project_tags']
                clicked_tags = res[0]['tags']
                clicked_body = res[0]['body']


                // put the right parts of the result into the right boxes.
                // Put tags and proj tags as options into select boxes
                let tag_array = []

                for (let tag of clicked_tags)
                    tag_array.push('<option selected="selected">' + tag + '</option>');

                $("#tags_clicked").html(tag_array);


                $('#project_tags_clicked').html('<div class="doris-sr pt-2" id="project_tags_content">' + clicked_proj_tags.join(", ") + '</div>');
                // $('#tags_clicked').html('<div class="doris-sr pt-2" id="tags_content">' + clicked_tags.join(", ") + '</div>');
                quill.setText(clicked_body);

                clicked_id = res[1]

            }
    });
}




function highlightResult(x) {
    // add a bg-light class to the div
    x.setAttribute("class", "bg-light doris-sr border border-dark m-2 pl-1")
}

function unhighlightResult(x) {
    // replace the bg-white to the div
    x.setAttribute("class", "bg-white doris-sr border border-dark m-2 pl-1")
}

  var quill = new Quill('#editor', {
    theme: 'snow'
  });

$('#update_entry_btn').click(function(){
    // retrieve tags from select box
    // put them into a list to send via JSON
    let new_tags_data = $("#tags_clicked").select2('data');
    console.log(new_tags_data)
    let new_tags = [];
    for (let i of new_tags_data)
        new_tags.push(i['text']);

    // retrieve project tags from select box.
    // put them into a list to send via JSON
    let new_proj_tags_data = $("#project_tags_clicked").select2('data');
    let new_project_tags = [];
    for(let i of new_proj_tags_data)
        new_project_tags.push(i['text']);

    let new_body = quill.getText();
    console.log(new_tags);


    // let update_object = {"project_tags_new": proj_tags, "tags_new": tags, "body_new": body }

    // ajax query to send to application.py
    // send the data as **kwargs for update method?
    // will tags and proj tags be lists?
    // send json over ajax. What do I need it to look like?
    // id=clicked_id, new_project_tags=proj_tags_new, new_tags=tags_new, new_body=body_new



});
