$('#search_entries_btn').click(function(){


     // define query object - a dictionary
let query_object = { "query": {   }}
// if tags and/or project tags checked: query object = { query: { term: { tags: "text", project_tags:
// "text" }}}
let tagsCheckbox = $('#search_tags_check');
let projTagsCheckbox = $('#search_proj_tags_check');
let bodyCheckbox = $('#search_body_check')
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
        //this only works when tags and project_tags are lists. They're not all currently in the test instance, but they
        //must be in the final edition. That needs to be a feature of real Doris
        result_array.push('<div class="border border-dark m-2 pl-1">Tags: ' + res['tags'].join(", ") +
            '<br>Project ' +
        'Tags: ' + res['project_tags'].join(", ") + '<br>Body: ' + res['body'] + '<br>Date: ' + res['date']);


    // Currently if there's an error, the previous results will display in the search_results window. I want to make
        // it so that that will clear to make it more user friendly.
    $('#search_results').html(result_array);




      }, error: function (){
      alert("Nothing is happening");
      } });
});