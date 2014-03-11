var HOST = "http://127.0.0.1:41021";
var AUTHENTICATED_USER = "AUTHUSERHASH1234";
var csrftoken = getCookie('csrftoken');

console.log(csrftoken);

$(document).on('ready', function(){
	$('.newPost').on('click', function(){$('#newPostModal').modal() });
	$('.friendRequest .acceptFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "accept", console.log) });
	$('.friendRequest .rejectFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "reject", console.log) });
    $('#newPostForm .post_type').on("change", function(){console.log($(this).val()); $(this).val() == "image" ? $('#newPostForm .image_field').removeClass('hide') : $('#newPostForm .image_field').addClass('hide') });
    $('#createPost').on('click', createPostGlobal);
    $('#btn-login').on('click', submitLogin);
});


function getActivityStream(callback){
	$.get("/author/posts", function(data){callback(data)}, "json");
}

function getUserPost(callback, userid){
	$.get("/author/"+userid+"/posts", function(data){callback(data)}, "json");
}


function processFriend(friendid, action, callback){
	alert('Processing Friend Request From: ' + friendid + " action: " + action)
	if(action == "accept"){
		//Accept friend request by sending it to ourselves?
		//should validate author id serverside
		var data = {"query":"friendrequest",
						"author":{
						"id": AUTHENTICATED_USER,
						"host":"http://127.0.0.1:5454/",
						"displayname":"Greg"
						},
						"friend": 	{
						                 "id":friendid,
						                 "host":"http://127.0.0.1:5454/",
						                 "displayname":"Lara",
						                 "url":"http://127.0.0.1:5454/author/" + friendid
						            }
						}
		$.post('/friendrequest', data, callback);
		
	}else{
		//reject friend request, need a function
		$.ajax({
		  type: "DELETE",
		  url: "/friends/"+AUTHENTICATED_USER+"/"+friendid,
		  success: callback
		});
	}
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
    $.post("/post/create/", data, callback, "json");
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submitLogin(callback){
	var data = $('#loginform').serialize();
	$.post("/accounts/login/", data, function(){
		window.location = "/";
	})
}

function submitLogin(callback){
	var data = $('#loginform').serialize();
	$.post("/accounts/login/", data, function(){
		window.location = "/";
	})
}
