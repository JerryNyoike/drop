let skip = 0;
let player_open = false;
$(window).ready(function() {

	getNewBeats();
	getRecentlyViewed();

});

function getNewBeats(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/fetch/recent';

	let headers = new Headers();
	headers.append("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

	const options = {
		method: 'GET',
		headers: headers
	}
	
    fetch(url, options)
        .then(response => response.json())
        .then(function (response) {
			$('.loading').css("display", "none");
            if (response.status == 1) {
                populateBeatsBody(response.beats, '#new-releases');
				$('.new-releases .empty').css("display", "none");
				$('.new-releases #new-releases').css("display", "flex");
            } else {
				$('.new-releases #new-releases').css("display", "none");
				$('.new-releases .empty').css("display", "block");
            	$('.home .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
			$('.loading').css("display", "none");
			showPrompt("Something went wrong", 0);
            console.log(error);
        });
}

function getRecentlyViewed(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/fetch/in?limit=' + beat_request_limit + '&skip=' + skip;

	let headers = new Headers();
	headers.append("Content-Type", 'application/json');
	headers.append("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

	var viewed = localStorage.getItem('viewed') ? JSON.parse(localStorage.getItem('viewed')) : [];
	let body = {
		beat_ids: viewed
	}

	const options = {
		method: 'POST',
		headers: headers,
        body: JSON.stringify(body)
	}

    fetch(url, options)
        .then(response => response.json())
        .then(function (response) {
			$('.loading').fadeOut("fast");
            if (response.status == 1) {
                populateBeatsBody(response.beats, "#recents");
				$('.recents #recents').css("display", "flex");
				$('.recents .empty').css("display", "none");
            } else {
				$('.recents #recents').css("display", "none");
				$('.recents .empty').css("display", "block");
				$('.recents .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
            console.log(error);
			$('.loading').fadeOut("fast");
			$('.beats').append('<p style="text-align: center">Something went wrong</p>');
        });
}
