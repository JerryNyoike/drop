let skip = 0;
let player_open = false;
let genres = [];
$(window).ready(function() {

	checkPreferences();

	$(document).on('click', '.preference-item', function(){
		const id = $(this).attr('id');
		const radio = $('#radio' + id);
		const genre = $('#' + id + ' p').text();
		if (radio.attr('class').includes("selected")) {
			$(radio).removeClass('fa-dot-circle-o');
			$(radio).addClass('fa-circle-o');
			radio.toggleClass("selected");
			genres.splice(genres.indexOf(genre), 1);
		} else {
			$(radio).removeClass('fa-circle-o');
			$(radio).addClass('fa-dot-circle-o');
			radio.toggleClass("selected");
			genres.push(genre);
		}
	});

	$('#save-genres').on('click', function(event) {
		event.preventDefault();
		if (genres) localStorage.setItem("genre-preferences", JSON.stringify(genres));
		$('.preferences').fadeOut();
		$('.beats').fadeIn();	
		getBeats();
	});

});

function checkPreferences(){
	if (!localStorage.getItem("genre-preferences")) {
		$('.beats').fadeOut('fast');
		$('.preferences').fadeIn('fast');
		getGenres();
	} else {
		$('.preferences').fadeOut('fast');
		$('.beats').fadeIn('fast');
		getBeats();
	}
}

function getGenres(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/genres';

    fetch(url, {method: 'GET'})
        .then(response => response.json())
        .then(function (response) {
			$('.loading').fadeOut("fast");
            if (response.status == 1) {
                addPreferences(response.genres);
            } else {
            	showPrompt(response.message, response.status);
				$('.preferences').fadeOut('fast');
				$('.beats').fadeIn('fast');
				getBeats();
            }
        })
        .catch(function (error) {
            console.log(error);
			$('.loading').fadeOut("fast");
			$('.preferences').fadeOut();
			$('.beats').fadeIn();
			$('.beats').append('<p style="text-align: center">Something went wrong</p>');
        });
}

function addPreferences(genres){
	for (var i = 0; i < genres.length; i++) {
		const genre = genres[i].genre;
		const r = Math.floor(Math.random() * 255);
		const g = Math.floor(Math.random() * 255);
		const b = Math.floor(Math.random() * 255);
		let div = `
		<div class="preference-item" id="${i}" style="background-color: rgb(${r}, ${g}, ${b})">
			<p>${genre}</p>
			<span class="fa fa-circle-o" id="radio${i}"></span>
		</div>`;
		$('.genres').append(div);
	}
}

function getBeats(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/fetch/all?limit=' + beat_request_limit + '&skip=' + skip;

    fetch(url, {method: 'GET'})
        .then(response => response.json())
        .then(function (response) {
			$('.loading').fadeOut("fast");
            if (response.status == 1) {
                populateBeatsBody(response.beats);
            } else {
				$('.beats').append('<p style="text-align: center">No beats found</p>');
            }
        })
        .catch(function (error) {
            console.log(error);
			$('.loading').fadeOut("fast");
			$('.beats').append('<p style="text-align: center">Something went wrong</p>');
        });
}

function populateBeatsBody(beats){
	$('.beats').empty();
	for (var i = 0; i < beats.length; i++) {
		const beat = beats[i];
		const photo = beat_images[Math.floor(Math.random() * 10)];
		const genre_id = beat.genre.toLowerCase().split(' ').join('_');

		let anim_class = 'zoom-in';
		if (i < 20) anim_class = 'zoom_in';
		
		checkGenreDiv(beat.genre, genre_id);
		const div = `
		<div class="flex-bg-20 flex-md-30 flex-xs-50">
			<div class="beat-item ${anim_class}">
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
		$('#' + genre_id).append(div);
	}
}

function checkGenreDiv(genre, genre_id){
	if ($('#' + genre_id).length < 1) {
		let element = `
		<div class="genre">
			<h2>${genre}</h2>
			<a class="see-all" href="explore/${genre_id}">See all</a>
			<div class="row" id="${genre_id}">
				<!-- Beats appended here -->
			</div>
		</div>`;
		$('.beats').append(element);
	}
}
