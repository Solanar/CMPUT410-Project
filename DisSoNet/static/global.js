
$(document).on('ready', function(){
	$('.newPost').on('click', function(){$('#newPostModal').modal() });
	$('.friendRequest .acceptFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "accept") });
	$('.friendRequest .rejectFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "reject") });
    $('#newPostForm .post_type').on("change", function(){console.log($(this).val()); $(this).val() == "image" ? $('#newPostForm .image_field').removeClass('hide') : $('#newPostForm .image_field').addClass('hide') });
    $('#createPost').on('click', createPostGlobal);
});


function getActivityStream(callback){
	$.get("/author/posts", function(data){callback(data)}, "json");
}

function getUserPost(callback, userid){
	$.get("/author/"+userid+"/posts", function(data){callback(data)}, "json");
}


function processFriend(friendid, action){
	alert('Processing Friend Request From: ' + friendid + " action: " + action)
}

function createPostGlobal(){
    var data = $('#newPostForm').serialize();
    /*TODO Massage form data here to meet server spec*/
    alert("Posting the following to /posts \n" + data);
    sendPost(data, console.log);
    $('#newPostModal').modal("close");
}


function sendPost(data, callback){
    /*
    Fields from JSON example_artivle.json
    title: Title of the post
    source: The URL of where we got the post
    origin: The URL of where it actually came from
    description: Brief description of the post, limited by characters of 100
    content-type: choice of [text/html, text/x-markdown, text/plain]
    content: Text field to input the contents of the post
    author: Foreign key referenceing author 
    */
    $.post("/posts", data, callback, "json");
}