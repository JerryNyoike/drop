$(document).ready(function(){
    $('#profile-image').attr('src', '/static/assets/images/profile.png');
    $('#select-img, #profile-image').on('click', function(){
        $("#file").trigger("click");
    });

    $("#file").change(function() {
        readURL(this);
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            const img = $('#profile-image');
            img.attr('src', e.target.result);
            img.css("padding", "0");
            img.css("width", "70px");
            img.css("height", "70px");
        }

        reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}