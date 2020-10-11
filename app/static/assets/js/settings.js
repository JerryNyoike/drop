const active_tab = localStorage.getItem('active-tab') ? localStorage.getItem('active-tab') : "profile";
$(document).ready(function(){
	switchTab(active_tab);
	$('.tab').on('click', function(){
		const id = $(this).attr('id');
		switchTab(id);
	});
});

function switchTab(id){
	$('.profile, .connected, .notification-settings, .account, .payments').css('display', 'none');
	$('.tab').each(function(){
		$(this).removeClass('active');
	});
	$('#' + id).addClass('active');
	$('.settings .' + id).fadeIn('fast');
	localStorage.setItem('active-tab', id);
}
