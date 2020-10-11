$(document).ready(function(){

});

function upload(){
	const url = server + "beat/upload";
	const file = document.forms.register_form.file;

	var formdata = new FormData();
	formdata.append("file", file.files[0], file.files[0].name);
	formdata.append("name", document.forms.beat_form.name.value);
	formdata.append("category", document.forms.beat_form.category.value);
	formdata.append("leasePrice", document.forms.beat_form.leasePrice.value);
	formdata.append("sellingPrice", document.forms.beat_form.sellingPrice.value);

	let headers = new Headers();
	headers.append("X-CSRFToken", csrf_token);

	var requestOptions = {
	  method: 'POST',
	  headers: headers,
	  body: formdata
	};

	fetch(, requestOptions)
		.then(response => response.json())
		.then(result => {

		})
		.catch(error => {
			console.log('Error', error);
		});
}