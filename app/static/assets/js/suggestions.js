let skip = 0;
let player_open = false;
let categories = [];
$(window).ready(function() {

	checkPreferences();

	$(document).on('click', '.preference-item', function(){
		const id = $(this).attr('id');
		const radio = $('#radio' + id);
		const category = $('#' + id + ' p').text();
		if (radio.attr('class').includes("selected")) {
			$(radio).removeClass('fa-dot-circle-o');
			$(radio).addClass('fa-circle-o');
			radio.toggleClass("selected");
			categories.splice(categories.indexOf(category), 1);
		} else {
			$(radio).removeClass('fa-circle-o');
			$(radio).addClass('fa-dot-circle-o');
			radio.toggleClass("selected");
			categories.push(category);
		}
	});

	$('#save-categories').on('click', function(event) {
		event.preventDefault();
		if (categories) localStorage.setItem("category-preferences", JSON.stringify(categories));
		$('.preferences').fadeOut();
		$('.beats').fadeIn();	
		getBeats();
	});

});

function checkPreferences(){
	if (!localStorage.getItem("category-preferences")) {
		$('.beats').fadeOut('fast');
		$('.preferences').fadeIn('fast');
		getcategories();
	} else {
		$('.preferences').fadeOut('fast');
		$('.beats').fadeIn('fast');
		getBeats();
	}
}

function getcategories(){
	$('.loading').fadeIn("fast");
	const url = server + 'beat/categories';

    fetch(url, {method: 'GET'})
        .then(response => response.json())
        .then(function (response) {
			$('.loading').fadeOut("fast");
            if (response.status == 1) {
                addPreferences(response.categories);
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

function addPreferences(categories){
	for (var i = 0; i < categories.length; i++) {
		const category = categories[i].category;
		const r = Math.floor(Math.random() * 255);
		const g = Math.floor(Math.random() * 255);
		const b = Math.floor(Math.random() * 255);
		let div = `
		<div class="preference-item" id="${i}" style="background-color: rgb(${r}, ${g}, ${b})">
			<p>${category}</p>
			<span class="fa fa-circle-o" id="radio${i}"></span>
		</div>`;
		$('.categories').append(div);
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
		const category_id = beat.category.toLowerCase().split(' ').join('_');

		let anim_class = 'zoom-in';
		if (i < 20) anim_class = 'zoom_in';
		
		checkcategoryDiv(beat.category, category_id);
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
		$('#' + category_id).append(div);
	}
}

function checkcategoryDiv(category, category_id){
	if ($('#' + category_id).length < 1) {
		let element = `
		<div class="category">
			<h2>${category}</h2>
			<a class="see-all" href="category/${category_id}">See all</a>
			<div class="row" id="${category_id}">
				<!-- Beats appended here -->
			</div>
		</div>`;
		$('.beats').append(element);
	}
}
