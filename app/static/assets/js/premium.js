$(document).ready(function(){

	getTestimonials();

	$(document).on('click', '.indicators a', function(event){
		const id = $(this).attr('id');
		moveCarousel(id.split('-')[1]);
	});

	$('.crumb').on('click', function(event){
		var hash = this.hash;
		console.log(hash);
		if (hash != "") 
		{
			event.preventDefault();
			$('html, body').animate({
				scrollTop : $(hash).offset().top
			},900,function(){
				window.location.hash = hash;
			});
		}
	});

});

function getTestimonials() {
	// $('.loading').fadeIn("fast");
	// const url = server + 'beat/fetch/genre/' + genre + '?limit=' + beat_request_limit + '&skip=' + skip;

 //    fetch(url, {method: 'GET'})
 //        .then(response => response.json())
 //        .then(function (response) {
	// 		$('.loading').fadeOut("fast");
 //            if (response.status == 1) {
 //                populateBeatsBody(response.beats);
 //            } else {
 //            	showPrompt(response.message, response.status);
 //            }
 //        })
 //        .catch(function (error) {
 //            console.log(error);
	// 		$('.loading').fadeOut("fast");
 //        });
        
	const testimonials = [
		{
			profile_img: "nyashinski.jpg",
			name: "Nyashinski", 
			testimonial: "Lorem ipsum dolor sit amet, semper cetero iisque in usu. Sit vocent fuisset consequat ei, at wisi possim sea, utamur lobortis torquatos id sit. Has te bonorum consequat, at dicunt placerat eam, vocibus necessitatibus ei eos. Sea malorum forensibus ne, an mea habeo option copiosae, congue labores eu qui."
		},
		{
			profile_img: "kaligraph.jpg",
			name: "Kaligraph", 
			testimonial: "Lorem ipsum dolor sit amet, semper cetero iisque in usu. Sit vocent fuisset consequat ei, at wisi possim sea, utamur lobortis torquatos id sit. Has te bonorum consequat, at dicunt placerat eam, vocibus necessitatibus ei eos. Sea malorum forensibus ne, an mea habeo option copiosae, congue labores eu qui."
		},
		{
			profile_img: "octo.jpg",
			name: "Octopizzo", 
			testimonial: "Lorem ipsum dolor sit amet, semper cetero iisque in usu. Sit vocent fuisset consequat ei, at wisi possim sea, utamur lobortis torquatos id sit. Has te bonorum consequat, at dicunt placerat eam, vocibus necessitatibus ei eos. Sea malorum forensibus ne, an mea habeo option copiosae, congue labores eu qui."
		},
		{
			profile_img: "kaligraph.jpg",
			name: "Nyashinski", 
			testimonial: "Lorem ipsum dolor sit amet, semper cetero iisque in usu. Sit vocent fuisset consequat ei, at wisi possim sea, utamur lobortis torquatos id sit. Has te bonorum consequat, at dicunt placerat eam, vocibus necessitatibus ei eos. Sea malorum forensibus ne, an mea habeo option copiosae, congue labores eu qui."
		}
	];
	populateCarousel(testimonials);
}

function populateCarousel(testimonials){
	let row = 0;
	let count = 1;
	for (var i = 0; i < testimonials.length; i++) {
		if (((i + 1) % 2) !== 0) {
			row++;
			$('.caroussel-body').append(`<div class="row" id="row-${row}"></div>`);
			$('.indicators').append(`<span class="fa fa-circle" id="indi-${row}"></span>`);
		}
		if (count > 2) count = 1;
		addTestimonial(testimonials[i], row, count);
		count++;
	}
	let row_count = 1;
	moveCarousel(row_count);
	row_count++;
	setInterval(function(){
		moveCarousel(row_count);
		row_count++;
		if (row_count > $('.caroussel-body').children().length) row_count = 1;
	}, 7000);
}

function addTestimonial(testimonial, row, count){
	let anim_class = 'slide_from_left';
	if (count === 2) anim_class = 'slide_from_right';
	let div = `		
	<div class="flex-bg-50 flex-md-100">
		<div class="testimonial ${anim_class}" id="testimonial${count}">
			<img src="resource/images/${testimonial.profile_img}">
			<div class="testimony">
				<h3>${testimonial.name}</h3>
				<p><span class="fa fa-quote-left"></span>${testimonial.testimonial}<span class="fa fa-quote-right"></span></p>
			</div>
		</div>
	</div>`;
	$('#row-' + row).append(div);
}

function moveCarousel(row){
	$('#testimonial1, #testimonial2').each(function(){
		$(this).removeClass('slide_from_left');
		$(this).removeClass('slide_from_right');
	});
	$('#testimonial1, #testimonial2').addClass('zoom_out');
	setTimeout(function(){
		$('#testimonial1, #testimonial2').each(function(){
			$(this).removeClass('zoom_out');
		});
		$('.caroussel-body .row').each(function(){
			$(this).css('display', 'none');
		})
		$('.indicators span').each(function(){
			$(this).removeClass('active');
		});
		$('#row-' + row).fadeIn();
		$('#indi-' + row).addClass('active');
		$('#row-' + row + ' #testimonial1').addClass('slide_from_left');
		$('#row-' + row + ' #testimonial2').addClass('slide_from_right');
	}, 300);
}