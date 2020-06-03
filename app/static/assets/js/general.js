let navCollapsed = false;
let navbarOpen = false;
$(document).ready(function(){
    $('.navbar a, .to-top a').on('click', function(event){
		var hash = this.hash;
		if (hash != "") 
		{
			event.preventDefault();
			$('html, body').animate({
				scrollTop : $(hash).offset().top
			}, 600, function(){
				window.location.hash = hash;
			});
		}
    });

    $(window).scroll(function(){
        var winTop = $(window).scrollTop();

        $('.slide-from-top').each(function(){
            var pos = $(this).offset().top;
            if (pos < winTop + 600) {
                $(this).addClass("slide_from_top");
            }
        });

        $('.slide-from-left').each(function(){
            var pos = $(this).offset().top;
            if (pos < winTop + 600) {
                $(this).addClass("slide_from_left");
            }
        });

        $('.slide-from-right').each(function(){
            var pos = $(this).offset().top;
            if (pos < winTop + 600) {
                $(this).addClass("slide_from_right");
            }
        });

        $('.zoom-in').each(function(){
            var pos = $(this).offset().top;
            if (pos < winTop + 600) {
                $(this).addClass("zoom_in");
            }
        });
    });

    $(".dropdown-toggle").on('click', function(event){
        event.preventDefault();
        $(".dropdown_menu").slideToggle();
    });

    $('.navbar-collapse').on('click', function(){
        if (navCollapsed) {
            $('.navbar').css("display", "block");
            $('.container').css("margin-left", "");
            $('.navbar').animate({
                left: '0'
            }, 300, function(){
                $('.navbar-minimal').css("display", "none");
                $('.navbar').css("display", "block");
                $('.container').css("width", "");
                $('.navbar-collapse span').removeClass('fa-chevron-right');
                $('.navbar-collapse span').addClass('fa-chevron-left');
                navCollapsed = false;
            });
        } else {       
            $('.navbar-minimal').css('display', 'block');   
            $('.navbar').animate({
                left: '-20%'
            }, 300, function(){
                $('.navbar').css("display", "none");
                $('.container').css("width", "94%");
                $('.container').css("margin-left", "6%");
                $('.navbar-collapse span').removeClass('fa-chevron-left');
                $('.navbar-collapse span').addClass('fa-chevron-right');
                navCollapsed = true;
            });
        }
    });

    $('.navbar-toggle').on('click', function(){
        if (navbarOpen) {
            $('nav').animate({
                left: '-80%'
            }, 500, function(){
                $('nav').css("display", "none");
                $('.navbar-toggle span').removeClass('fa-close');
                $('.navbar-toggle span').addClass('fa-bars');
            });
            navbarOpen = false;
        } else {
            $('nav').css("display", "block");
            $('nav').css("left", "-80%");
            $('nav').animate({
                left: '0'
            }, 500);
            $('.navbar-toggle span').removeClass('fa-bars');
            $('.navbar-toggle span').addClass('fa-close');
            navbarOpen = true;
        }
    });

    get_user_session();

    var d = new Date();
    var n = d.getFullYear();
    $('#year').text(n);

});

function get_user_session(){
    if(localStorage.user_details != "" && localStorage.user_details != null){
        let user_details = JSON.parse(localStorage.user_details);
        $("#login-link").css("display", "none");
        $('#register-link').css("display", "none");
        $('#username').css("display", "inline-block");
        $('#username').text(user_details.name);
    }
}

function logout(){
    localStorage.setItem("user_details", ""); 
    window.location.assign("index.html");   
}

function showPrompt(message, state){
    if (state == 0){
        $("#prompt-icon").removeClass("fa-check");
        $("#prompt-icon").addClass("fa-close");
    }
    $(".prompt-message").text(message);
    $(".prompt").fadeToggle();
    setTimeout(function(){
        $(".prompt").fadeToggle();
    }, 2000);
}

