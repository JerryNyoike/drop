let cartItems = localStorage.getItem("cart") ? JSON.parse(localStorage.getItem("cart")) : {};

$(document).ready(function(){

	$(document).on('click', '.reduce', function(event){
		event.preventDefault();
		const id = $(this).attr('id');
		reduceQuantity(id);
	});

	$(document).on('click', '.delete', function(event){
		event.preventDefault();
		const id = $(this).attr('id');
		deleteItem(id);
		// openPwdialog(id);
	});

	document.getElementById("print").onclick = function(event){
		event.preventDefault();
		if (!isEmptyObject(cartItems)) submitSale();
	};

	$('#close-pwdialog').on('click', closePwdialog);
});

function populateCart(newbeat = {}){
	$('#cart-body').empty();
	if (!isEmptyObject(cartItems)){
		for (beat_id in cartItems){
			addRow(cartItems[beat_id]);	
		}
	}
	if (!isEmptyObject(newbeat)) {
		addCartItem(newbeat);
	}
}

function addRow(beat){
	let div = `
	<div class="trow" id="row${beat.beat_id}">

	</div>`;
	$('#cart-body').append(div);
	if (beat.quantity > 1){
		updatePrice(beat.beat_price, beat.quantity);
	} else {	
		updatePrice(beat.beat_price);
	}
}

function addCartItem(beat){
	beat.quantity = 1;
	if (!cartItems.hasOwnProperty(beat.beat_id)){
		cartItems[beat.beat_id] = beat;
		localStorage.setItem('cart', JSON.stringify(cartItems));
		addRow(beat);
	} else {	
		const element = $("#row" + beat.beat_id + " #quantity");
		let quantity = parseInt(element.text());
		cartItems[beat.beat_id].quantity = ++quantity;
		localStorage.setItem('cart', JSON.stringify(cartItems));
		element.text(quantity);
		updatePrice(beat.beat_price);
	}
}

function deleteItem(id){
	if (!isEmptyObject(cartItems)){	
		if (cartItems[id].quantity > 1){
			updatePrice(-cartItems[id].beat_price, cartItems[id].quantity);
		} else {
			updatePrice(-cartItems[id].beat_price);
		}
		delete cartItems[id];
		localStorage.setItem('cart', JSON.stringify(cartItems));
		$('#row' + id).detach();
		if (isEmptyObject(cartItems)){
			$('#cart-body').append(`<div class="trow"><p class="tdata">No Items in the cart<p></div>`);
		}
	}
}

function updatePrice(beatPrice, quantity = 1, beatDiscount = 0){
	let sub_total = parseFloat($('#sub-total').text());
	let vat_sub_total = parseFloat($('#vat-sub-total').text());
	let discount = parseFloat($('#discount').text());
	let total = parseFloat($('#total').text());

	sub_total += (beatPrice * quantity * 0.84);
	$('#sub-total').text(sub_total);

	vat_sub_total += (beatPrice * quantity * 0.16);
	$('#vat-sub-total').text(vat_sub_total);

	discount += (beatPrice * quantity * beatDiscount);
	$('#discount').text(discount);

	total = ((sub_total + vat_sub_total) - discount);
	$('#total').text(total);
}

function checkout() {
	const url = server + "sales";

	let headers = new Headers();
	headers.append("X-CSRFToken", csrf_token);
	headers.append("Content-Type", "application/json");

	const payment_method = $("input[name='payment_method']").val();
	if(!payment_method) {
		showPrompt("Choose payment method", 0);
		return;
	}

	let requestBody = {
		beats: cartItems,
		total : $('#total').text(),
		payment_method : payment_method
	};

	let requestOptions = {
		method: 'POST',
		headers: headers,
		body: JSON.stringify(requestBody)
	};

	fetch(url, requestOptions)
		.then(response => response.json())
		.then(result => {
			if (result.status == 1){
				window.location.assign("/sales");
		  	} else {
		  		showPrompt(result.message, 0);
		  	}
		})
		.catch(error => {
	  		showPrompt("Something went wrong", 0);
			console.log('error', error);
		});
}

function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires="+ d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}