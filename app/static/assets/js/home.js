let skip = 0;
let player_open = false;
$(window).ready(function() {

	getBeats();
	
	$(".play").on("click", function(event){
		event.preventDefault();
	});

	$("#play").on('click', function(){
		
	});

});

function getBeats(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/fetch/all?limit=' + beat_request_limit + '&skip=' + skip;

    fetch(url, {method: 'GET'})
        .then(response => response.json())
        .then(function (response) {
			$('.loading').css("display", "none");
            if (response.status == 1) {
                populateBeatsBody(response.beats);
            } else {
            	showPrompt(response.message, response.status);
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

function populateBeatsBody(beats){
	for (var i = 0; i < beats.length; i++) {
		const beat = beats[i];
		const photo = beat_images[Math.floor(Math.random() * 10)];

		let anim_class = 'zoom-in';
		if (i < 20) anim_class = 'zoom_in';
		
		const div = `
		<div class="flex-bg-20 flex-md-30 flex-xs-50">
			<div class="beat-item ${anim_class}" id="${beat.beat_id}">
				<div class="image">
					<img src="${photo}">
					<div class="overlay"></div>
				</div>
				<a href="/beat/${beat.beat_id}" class="play"><span class="fa fa-play"></span></a>
				<p class="date">${beat.upload_date}</p>
				<div class="beat-details">
					<h3>${beat.name}</h3>
					<p>${beat.producer}</p>
				</div>
			</div>
		</div>`;
		$('#new-releases').append(div);
		$('#recents').append(div);
	}
}
