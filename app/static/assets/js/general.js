let navCollapsed = false;
let navbarOpen = false;
let dropdownOpen = false;
$(document).ready(function(){
    $('.loading').css("display", "none");

    checkNav();

    $('nav a, .nav-right ul li a, .dropdown-item a').on('click', function(event) {
        event.preventDefault();
        const href = $(this).attr('href');
        const id = $(this).attr('id');
        const visited = localStorage.getItem('visited') ? JSON.parse(localStorage.getItem('visited')) : [];
        if (!visited.includes(id)) {
            visited.push(id);
            localStorage.setItem('visited', JSON.stringify(visited));
            $('#' + id).each(function(){
                $(this).addClass('visited');
            });
        }
        window.location.assign(href);
    });

    $('.to-top a').on('click', function(event){
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

    $(window).scroll(onScroll);

    window.onclick = function(event){   
        if (dropdownOpen) {   
            $.each([1, 2], function(i, val){  
                $('#dropdown-item-' + val).animate({
                    top: '0',
                }, 300, function(){
                    $("#dropdown-item-" + val).css("display", "none");
                });
            });
            dropdownOpen = false;
        }
    };

    $(".dropdown-toggle").on('click', toggleDropdown);

    $('.navbar-collapse').on('click', collapseNav);

    $('.navbar-toggle').on('click', toogleNavBar);

    $('#toggle-notifications').on('click', function(event){
        event.preventDefault();
        $('.notifications-dialog').fadeToggle();
    });

    collapsibleFeatures();

    check_user_session();

    var d = new Date();
    var n = d.getFullYear();
    $('#year').text(n);

});

function onScroll(){
    var winTop = $(window).scrollTop();

    $('.slide-from-top').each(function(){
        var pos = $(this).offset().top;
        if (pos < winTop + 800) {
            $(this).addClass("slide_from_top");
        }
    });

    $('.slide-from-left').each(function(){
        var pos = $(this).offset().top;
        if (pos < winTop + 800) {
            $(this).addClass("slide_from_left");
        }
    });

    $('.slide-from-right').each(function(){
        var pos = $(this).offset().top;
        if (pos < winTop + 800) {
            $(this).addClass("slide_from_right");
        }
    });

    $('.slide-from-bottom').each(function(){
        var pos = $(this).offset().top;
        if (pos < winTop + 800) {
            $(this).addClass("slide_from_bottom");
        }
    });

    $('.zoom-in').each(function(){
        var pos = $(this).offset().top;
        if (pos < winTop + 800) {
            $(this).addClass("zoom_in");
        }
    });

}

function checkNav(){
    let nav_collapsed = localStorage.getItem("nav-collapsed") ? localStorage.getItem("nav-collapsed") : "false";
    if (nav_collapsed == "true") {    
        $('.navbar-minimal').css('display', 'block');   
        $('.navbar').animate({
            left: '-50%'
        }, 300, function(){
            $('.navbar').css("display", "none");
            $('.container').css("width", "94%");
            $('.container').css("left", "6%");
            $('.navbar-collapse span').removeClass('fa-chevron-left');
            $('.navbar-collapse span').addClass('fa-chevron-right');
            navCollapsed = true;
        });
    }
    const visited = JSON.parse(localStorage.getItem('visited'));
    if (visited) {
        for (var i = visited.length - 1; i >= 0; i--) {
            $('#' + visited[i]).each(function(){
                $(this).addClass('visited');
            });
        }
    }
}

function collapseNav(){
    if (navCollapsed) {
        $('.navbar').css("display", "block");
        $('.container').css("left", "");
        $('.navbar').animate({
            left: '0'
        }, 300, function(){
            $('.navbar-minimal').css("display", "none");
            $('.navbar').css("display", "block");
            $('.container').css("width", "");
            $('.navbar-collapse span').removeClass('fa-chevron-right');
            $('.navbar-collapse span').addClass('fa-chevron-left');
            localStorage.setItem("nav-collapsed", "false");
            navCollapsed = false;
        });
    } else {       
        $('.navbar-minimal').css('display', 'block');   
        $('.navbar').animate({
            left: '-50%'
        }, 300, function(){
            $('.navbar').css("display", "none");
            $('.container').css("width", "94%");
            $('.container').css("left", "6%");
            $('.navbar-collapse span').removeClass('fa-chevron-left');
            $('.navbar-collapse span').addClass('fa-chevron-right');
            localStorage.setItem("nav-collapsed", "true");
            navCollapsed = true;
        });
    }
}

function toogleNavBar(){
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
}

function toggleDropdown(event){
    event.preventDefault();
    event.stopPropagation();
    if (dropdownOpen) {   
        $.each([1, 2], function(i, val){  
            $('#dropdown-item-' + val).animate({
                top: '0',
            }, 300, function(){
                $("#dropdown-item-" + val).css("display", "none");
            });
        });
        dropdownOpen = false;
    } else {     
        $(".dropdown-item").css("display", "flex");
        $.each([1, 2], function(i, val){  
            const top = (i * 50) + 'px';
            $('#dropdown-item-' + val).animate({
                top: top
            }, 300);
        });
        dropdownOpen = true;
    }
}

function collapsibleFeatures(){
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
    }
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

function check_user_session(){
    if(localStorage.user_details){
        let user_details = JSON.parse(localStorage.user_details);
        $("#login-link, #register-link").each(function(){
            $(this).css('display', 'none');
        });
        $('#profile-image').attr("src", server + "resource/images/" + user_details.profile_image);
        $('#profile-image').css("width", "40px");
        $('#profile-image').css("height", "40px");
        $('#profile-image').css("margin-top", "0");
    } else {
        $("#settings-link, #logout-link, #edit-link").each(function(){
            $(this).css('display', 'none');
        });
    }
}

function logout(){
    const url = server + 'client/logout';
    fetch(url, {method: "POST"})
        .then(response => response.json())
        .then(function(response) {
            if (response.status == 1) {
                localStorage.setItem("user_details", "");
                window.location.assign("/client/login");
            }
        })
        .catch(function (error){
            showPrompt("Something went wrong.Check your connection and try again", 0);
        });
    window.location.assign("/"); 
}