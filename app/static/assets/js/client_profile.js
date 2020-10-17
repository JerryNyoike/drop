let skip = 30;
$(document).ready(function(){
	getBeats();
	$('.tab').on('click', function(){
		const id = $(this).attr('id');
		switchTab(id);
	});

	$('#edit-link').on('click', function(event){
		event.preventDefault();
		localStorage.setItem('active-tab', 'profile');
		window.location.assign('/client/settings');
	});
});

function switchTab(id){
	$('.profile, .starred').css('display', 'none');
	$('.tab').each(function(){
		$(this).removeClass('active');
	});
	$('#' + id).addClass('active');
	$('.' + id).fadeIn('fast');
}

function getBeats(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/fetch/in?limit=' + beat_request_limit + '&skip=' + skip;

	let headers = new Headers();
	headers.append("Content-Type", 'application/json');
	headers.append("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

	var starred = localStorage.getItem('starred') ? JSON.parse(localStorage.getItem('starred')) : [];
	let body = {
		beat_ids: starred
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
                populateBeatsBody(response.beats, "#starred-body");
				$('.starred .beats').css("display", "block");
				$('.starred .empty').css("display", "none");
            } else {
				$('.starred .beats').css("display", "none");
				$('.starred .empty').css("display", "block");
				$('.starred .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
            console.log(error);
			$('.loading').fadeOut("fast");
			$('.beats').append('<p style="text-align: center">Something went wrong</p>');
        });
}

