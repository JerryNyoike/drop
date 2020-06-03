let skip = 0;
let player_open = false;
let player_collapsed = false;
$(window).ready(function() {

	getBeats();
	
	$(".play").on("click", function(event){
		event.preventDefault();
	});

	$("#play").on('click', function(){
		
	});

});

function getBeats(){
	const url = server + 'beat/fetch/all?limit=' + beat_request_limit + '&skip=' + skip;

    let headers = new Headers();
    headers.append("Authorization", "Bearer " + localStorage.token);

    let fetchData = {
        method: 'GET',
        headers: headers
    }

    fetch(url, fetchData)
        .then(response => response.json())
        .then(function (response) {
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
		let anim_class = 'zoom-in';
		if (i < 20) anim_class = 'zoom_in';
		const div = `
		<div class="flex-bg-20 flex-md-30 flex-xs-50">
			<div class="beat-item ${anim_class}" id="${beat.beat_id}">
				<div class="image">
					<img src="/static/assets/images/beat_img4.jpg">
					<div class="overlay"></div>
				</div>
				<a id="play"><span class="fa fa-play"></span></a>
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
