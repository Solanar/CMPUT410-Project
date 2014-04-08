var HOST = "http://127.0.0.1:41021";
var csrftoken = getCookie('csrftoken');

console.log(csrftoken);

$(document).on('ready', function(){
	$('.newPost').on('click', function(){$('#newPostModal').modal() });
	$('.githubForm').on('click', function(){$('#githubModal').modal() });
	$('.friendRequest .acceptFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "accept", console.log) });
	$('.friendRequest .rejectFriend').on("click", function(){ processFriend($(this).parents('.friendRequest').data('friendid'), "reject", console.log) });
    $('#newPostForm .post_type').on("change", function(){console.log($(this).val()); $(this).val() == "IMAGE" ? $('#newPostForm .image_field').removeClass('hide') : $('#newPostForm .image_field').addClass('hide') });
    $('#createPost').on('click', createPostGlobal);
    $('#btn-login').on('click', submitLogin);
    $('#btn-signup').on('click', submitSignup);
    $('.logout').on('click', actionLogout);
    $('.stream_post .btn-delete').on('click', function(){ deletePost( $(this).data('id'), $(this).parents('.stream_post').fadeOut() ) })
    $('.stream_post .btn-comment').on('click', function(){
    	$(this).css('display', 'none');
    	$(this).parents('.stream_post').find('.comment_input').slideDown().children('textarea').focus();
    	$(this).parents('.stream_post').find('.btn-post-comment').fadeIn();
   	});
    $('.stream_post .btn-post-comment').on('click', function(){
        sendComment($(this).data('id'), $(this).parents('.stream_post').find('textarea').val(), console.log);
    })
    if($('.stream_post').length > 0){renderPostTypes()};
    $('#addFriend').on('click', function(){processFriend($('#friendGUID').val(), "accept", console.log);});
});


function sendComment(guid, body, callback){
    var data = {"content" : body};
    $.ajax({
      type: "POST",
      url: '/posts/'+guid+'/comments/',
      data: data,
      beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: callback,
    });

}

$(document).on('submit', 'form.githubForm', function(form) {
  var $form = $(form);
  $.ajax({
    type: form.method,
    url: form.action,
    data: $form.serialize()
  });
});

function getActivityStream(callback){
	$.get("/author/posts", function(data){callback(data)}, "json");
}

function getUserPost(callback, userid){
	$.get("/author/"+userid+"/posts", function(data){callback(data)}, "json");
}


function processFriend(friendid, action, callback){
	//alert('Processing Friend Request From: ' + friendid + " action: " + action)
	if(action == "accept"){
		//Accept friend request by sending it to ourselves?
		//should validate author id serverside
		var data = {"query":"friendrequest",
						"author":{
							"id": AUTHENTICATED_USER,
						},
						"friend": 	{ "author" : {
						                 "id":friendid
						            }
						}}
		$.post('/friendrequest/', data, callback);

	}else{
		//reject friend request, need a function
		$.ajax({
		  type: "DELETE",
		  url: "/friends/"+AUTHENTICATED_USER+"/"+friendid+"/",
		  success: callback
		});
	}
}

function createPostGlobal(){
    var data = $('#newPostForm').serialize();
    /*TODO Massage form data here to meet server spec*/
    sendPost(data, function(data, text, xhr){
    	console.log("test");
    	console.log(xhr.getResponseHeader('Location'));
    	window.location =  xhr.getResponseHeader('Location');
    });
    $('#newPostModal').modal("hide");
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
    //    $.post("/post/create/", data, callback, "json");
    //    TODO: return should be json, but I forgive you
    $.post("/post/", data, callback);

}

//deletes a post
function deletePost(post_id, callback){
	$.ajax({
	  type: "DELETE",
	  url: "/post/"+post_id+"/",
      beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
	  success: callback,
	});
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

function submitLogin(event){
	var data = $('#loginform').serialize();
	$.post("/accounts/login/", data, function(){
		window.location = "/";
	})
}

function submitSignup(event){
	var data = $('#signupform').serialize();
	$.post("/accounts/register/", data, function(){
		window.location = "/";
	});
}

function actionLogout(event){
	$.get("/accounts/logout/", function(){
		window.location = "/";
	});
	event.preventDefault();
}

function renderPostTypes(){
    $('.stream_post').each(function(i,e){
        var post = $(this);
        var type = post.data('type');
        var content = post.find('.content');
        if(type == "HTML"){
            content.html(content.text());
        }
    })
}