function login(user_type){
    const type = user_type == 0 ? 'client' : 'producer';
    const url = server + type + '/login';

    let data = {
        email: document.forms.login_form.email.value,
        pwd: document.forms.login_form.password.value
    }

    let headers = new Headers();
    headers.append("Content-Type", "application/json");

    let fetchData = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    }

    fetch(url, fetchData)
        .then(response => response.json())
        .then(function (response) {
            if (response.status == 1) {
                showPrompt(response.message, response.status);
                localStorage.setItem("user_details", JSON.stringify(response.user_details));
                if (type === 'client'){
                    setTimeout(function(){
                        window.location.assign("/");
                    }, 1000);
                } else {
                    setTimeout(function(){
                        window.location.assign(server + "producer/");
                    }, 1000);
                }
            }
        })
        .catch(function (error) {
            showPrompt("Something went wrong.Check your connection and try again", 0);
            console.log(error);
        });
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