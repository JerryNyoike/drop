$(document).ready(function(){
	
	$(window).scroll(function(){
		let winTop = $(window).scrollTop();

		$('.portfolio').each(function(){
			var pos = $(this).offset().top;
			if (pos < winTop + 400) {					
				animateNumbers();
			}
		});

	});

});

function animateNumbers(){
	let highest = parseInt(document.querySelector('.highest').getAttribute("id"));
	const items = document.getElementsByClassName('counter');
	let interval = setInterval(function(){
		for (var i = items.length - 1; i >= 0; i--) {
			const element = items[i];
			const curr = parseInt(element.innerText);
			const count = parseInt(element.getAttribute("id"));
			if (curr < count) {
				element.innerText = parseInt(curr + parseInt(highest/100));
			} else {
				element.innerText = count;
			}		
			if (curr > highest) clearInterval(interval);
		}
	}, 250);	
}