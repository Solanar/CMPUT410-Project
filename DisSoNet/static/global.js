
$(document).on('ready', function(){
	$('.newPost').on('click', function(){$('#newPostModal').modal() });
	$('.friendRequest .acceptFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "accept") });
	$('.friendRequest .rejectFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "reject") });

});


function getActivityStream(callback){
	$.get("/author/posts", function(data){callback(data)}, "json");
}

function getUserPost(callback){
	$.get("/author/posts", function(data){callback(data)}, "json");
}

function sendPost(form){
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
	var data = form.serialize();

}

function processFriend(friendid, action){
	alert('Processing Friend Request From: ' + friendid + " action: " + action)
}