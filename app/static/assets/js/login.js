function login(user_type){
    var user_type = user_type == 0 ? 'client' : 'producer';
    const url = server + 'auth/login';

    let data = {
        email: document.forms.login_form.email.value,
        type: user_type,
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
            showPrompt(response.message, response.status);
            if (response.status == 1) {
                localStorage.setItem("token", response.payload);
                localStorage.setItem("user_details", JSON.stringify(response.user_details));
                if (user_type == "client"){
                    window.location.assign("index.html");
                } else {
                    window.location.assign("producer/index.html");
                }
            }
        })
        .catch(function (error) {
            showPrompt("Something went wrong.<br>Check your connection and try again")
        });
}

function showPrompt(message, state){
    console.log(state);
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