$(document).on('ready', function(){

	if($('#debugFriendMyGuid').length > 0){
		AUTHENTICATED_USER = $('#debugFriendMyGuid').text();
		console.log(AUTHENTICATED_USER);
	}

	$('#debugFriendBtn').on('click', function(){
		console.log("debug friend request");
		processFriend($('#debugFriendInput').val(), "accept", console.log);
	});
});