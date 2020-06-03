function register(user_type){
    var user_type = user_type == 0 ? 'client' : 'producer';
    const url = server + 'auth/register';

    password = document.forms.register_form.password.value;
    confirm_password = document.forms.register_form.confirm_password.value;

    if (password == confirm_password) {
        let data = {
            name: document.forms.register_form.names.value,
            email: document.forms.register_form.email.value,
            phone: document.forms.register_form.phone.value,
            type: user_type,
            pwd: password
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
                    setTimeout(function(){
                        if (user_type == "client") {
                            window.location.assign("login.html");
                        } else {
                            window.location.assign("producerlogin.html");
                        }
                    }, 2000);
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }
    else {
        showPrompt("Password do not match!!");
    }

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