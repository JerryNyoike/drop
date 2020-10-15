let navCollapsed = false;
let navbarOpen = false;
let dropdownOpen = false;
let notificationsOpen = false;
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

    $('a.crumb ,a.btn-pr, .to-top a').on('click', function(event){
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
            $(".dropdown-item").each(function(){  
                $(this).animate({
                    top: '0'
                }, 300, function(){
                    $(this).css("display", "none");
                });
            });
            dropdownOpen = false;
        }
        if (navbarOpen) {
            $('nav').animate({
                left: '-80%'
            }, 200, function(){
                $('nav').css("display", "none");
                $('.navbar-toggle span').removeClass('fa-close');
                $('.navbar-toggle span').addClass('fa-bars');
            });
            navbarOpen = false;
        }
        if (notificationsOpen) $('.notifications-dialog').fadeOut('fast');
    };

    $(".dropdown-toggle").on('click', toggleDropdown);

    $('.navbar-collapse').on('click', collapseNav);

    $('.navbar-toggle').on('click', toogleNavBar);

    $('#toggle-notifications').on('click', function(event){
        event.preventDefault();
        event.stopPropagation();
        $('.notifications-dialog').fadeToggle();
        if(notificationsOpen){
            notificationsOpen = false;
        } else {
            notificationsOpen = true;
        }
    });

    $('.copy-link').on('click', function(event){
        event.preventDefault();
        const link = $(this).attr('href');
        if (link) copyLink(server + link);
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
            setTimeout(function(){
                $(this).removeClass("zoom_in");
            }, 600);
        }
    });

}

function checkNav(){
    let nav_collapsed = localStorage.getItem("nav-collapsed") ? localStorage.getItem("nav-collapsed") : "false";
    if (nav_collapsed == "true") {    
        $('.navbar-minimal').css('display', 'block');   
        $('.navbar').animate({
            left: '-80%'
        }, 200, function(){
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
        $('.nav-right a span:nth-child(2), nav a span:nth-child(2)').each(function(){
            $(this).css('display', 'block');
        });
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
        }, 200, function(){
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
            left: '-80%'
        }, 200, function(){
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

function toogleNavBar(event){
    event.preventDefault();
    event.stopPropagation();
    if (navbarOpen) {
        $('nav').animate({
            left: '-80%'
        }, 200, function(){
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
        }, 200);
        $('.navbar-toggle span').removeClass('fa-bars');
        $('.navbar-toggle span').addClass('fa-close');
        navbarOpen = true;
    }
}

function toggleDropdown(event){
    event.preventDefault();
    event.stopPropagation();
    if (dropdownOpen) {   
        $(".dropdown-item").each(function(){  
            $(this).animate({
                top: '0'
            }, 300, function(){
                $(this).css("display", "none");
            });
        });
        dropdownOpen = false;
    } else {     
        $(".dropdown-menu").children().css("display", "flex");
        $(".dropdown-item").each(function(index){  
            const top = (index * 50) + 'px';
            $(this).animate({
                top: top
            });
        });
        dropdownOpen = true;
    }
}

function setCookie(cname, cvalue, exdays, httponly=false) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    var cookie = cname + "=" + cvalue + ";" + expires + ";path=/;Secure;SameSite=Lax;";
    if (httponly) cookie += "HttpOnly;"
    document.cookie += cookie;
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
    }
    return "";
}

function copyLink(link) {
    var textArea = document.createElement("textarea");
    textArea.style.visibility = 'hidden';
    textArea.value = link;
    document.body.appendChild(textArea);

    /* Select the text field */
    textArea.select();
    textArea.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    if(document.execCommand("copy")){
        /* Alert the copied text */
        showPrompt("Copied!", 1);
    }
    
    document.body.removeChild(textArea);
}

function populateBeatsBody(beats, parentId){
    const now = new Date();
    for (var i = 0; i < beats.length; i++) {
        const beat = beats[i];
        const photo = beat_images[Math.floor(Math.random() * 10)];

        let anim_class = 'zoom-in';
        if (i < 20) anim_class = 'zoom_in';

        // let categories_div = `<div class="categories">`;
        // for (var i = 0; i < beat.categories.length; i++) {
        //     categories_div += `
        //     <a href="category/${beat.categories[i].category}">
        //         <span class="fa fa-circle"></span>
        //         ${beat.categories[i].category}
        //     </a>`;
        // }
        // categories_div += `</div>`;
        
        const upload_date = compareDates(beat.upload_date);
        const div = `
        <div class="flex-bg-20 flex-md-30 flex-xs-50">
            <div class="beat-item ${anim_class}" id="${beat.beat_id}">
                <div class="image">
                    <img src="${photo}">
                    <div class="overlay"></div>
                </div>
                <a href="/beat/fetch/${beat.beat_id}" class="play"><span class="fa fa-play"></span></a>
                <p class="date">${upload_date}</p>
                <div class="beat-details">
                    <h3>${beat.name}</h3>
                    <p>By <a href="${server}producer/${beat.producer_id}"><b>${beat.producer}</b></p>
                </div>
            </div>
        </div>`;
        $(parentId).append(div);
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

function compareDates(upload_date){
    const now = new Date();
    const uploadDate = new Date(upload_date);
    if (now.getFullYear() ==  uploadDate.getFullYear()) {
        if (now.getMonth() == uploadDate.getMonth()) {
            if (now.getDate() == uploadDate.getDate()) {
                if (now.getHours() == uploadDate.getHours()) {
                    if (now.getMinutes() == uploadDate.getMinutes()) {
                        return "just now";
                    } else {
                        return (now.getMinutes() - uploadDate.getMinutes()) + " minutes ago";
                    }
                } else {
                    return (now.getHours() - uploadDate.getHours()) + " hours ago";
                }
            } else {
                return (now.getDate() - uploadDate.getDate()) + " days ago";
            }
        } else {
            return (now.getMonth() - uploadDate.getMonth()) + " months ago";
        }
    } else {
        return (now.getFullYear() - uploadDate.getFullYear()) + " years ago";
    }
    return upload_date;
}

function logout(){
    const url = server + 'client/logout';

    let headers = new Headers();
	headers.append("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

	const options = {
		method: 'GET',
		headers: headers
    }
    
    fetch(url, options)
        .then(response => response.json())
        .then(function(response) {
            if (response.status == 1) {
                localStorage.setItem("user_details", "");
                window.location.assign(server + "client/login");
            }
        })
        .catch(function (error){
            showPrompt("Something went wrong.Check your connection and try again", 0);
        });
    window.location.assign("/"); 
}