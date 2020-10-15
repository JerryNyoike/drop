let skip = 0;
let player_open = false;
$(window).ready(function() {

	getNewBeats();
	getRecents();

});

function getNewBeats(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/fetch/all?limit=' + beat_request_limit + '&skip=' + skip;

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
				$('.home .empty').css("display", "none");
            } else {
				$('.home .beats').css("display", "none");
            	$('.home .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
			$('.loading').css("display", "none");
			showPrompt("Something went wrong", 0);
            console.log(error);
        });
}

function getRecents(){
	const url = server + 'beat/fetch/all?limit=' + beat_request_limit + '&skip=' + skip;

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
                populateBeatsBody(response.beats, '#recents');
				$('.home .empty').css("display", "none");
            } else {
				$('.home .beats').css("display", "none");
            	$('.home .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
			$('.loading').css("display", "none");
			showPrompt("Something went wrong", 0);
            console.log(error);
        });
}