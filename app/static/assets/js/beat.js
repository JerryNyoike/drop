let skip = 0;
let player_open = false; 

function getBeats(category){
	$('.loading').fadeIn("fast");
	const url = server + 'category/' + category.toLowerCase().split(" ").join("_") + '?limit=' + beat_request_limit + '&skip=' + skip;

	let headers = new Headers();
	headers.append("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

	const options = {
		method: 'POST',
		headers: headers
	}

    fetch(url, options)
        .then(response => response.json())
        .then(function (response) {
			$('.loading').fadeOut("fast");
            if (response.status == 1) {
                populateBeatsBody(response.beats, '#beats-body');
				$('.related .beats').css("display", "block");
				$('.related .empty').css("display", "none");
            } else {
				$('.related .beats').css("display", "none");
				$('.related .empty').css("display", "block");
				$('.related .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
            console.log(error);
			$('.loading').fadeOut("fast");
        });
}


