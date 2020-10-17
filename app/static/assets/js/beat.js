let skip = 0;
let player_open = false; 

$(document).ready(function(){
	$('.star-beat').on('click', function(event){
		event.preventDefault();
		var starred = localStorage.getItem('starred') ? JSON.parse(localStorage.getItem('starred')) : [];
		var id = $(this).attr('id');
		if (starred.includes(id)) return;
		starred.push(id);
		localStorage.setItem("starred", JSON.stringify(starred));
		showPrompt("Starred", 1);
	});
	makeViewed();
});

function makeViewed(){
	var viewed = localStorage.getItem('viewed') ? JSON.parse(localStorage.getItem('viewed')) : [];
	var id = $('.star-beat').attr('id');
	if (viewed.includes(id)) return;
	if (viewed.length >= 15) {
		viewed = viewed.splice(1, 15);
		viewed.push(id);
		localStorage.setItem("viewed", JSON.stringify(viewed));
		return;
	}
	viewed.push(id);
	localStorage.setItem("viewed", JSON.stringify(viewed));
}

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


