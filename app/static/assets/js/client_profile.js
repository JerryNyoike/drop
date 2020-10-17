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
			$('.loading').fadeOut("fast");
            if (response.status == 1) {
				$('.starred .empty').css("display", "none");
                populateBeatsBody(response.beats, '#starred-body');
				$('.starred #starred-body').css("display", "flex");
            } else {
				$('.starred #starred-body').css("display", "none");
				$('.starred .empty').css("display", "block");
				$('.starred .empty .message').text(response.message);
            }
        })
        .catch(function (error) {
            console.log(error);
			$('.loading').fadeOut("fast");
        });
}
