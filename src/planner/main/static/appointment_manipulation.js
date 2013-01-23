"use strict";

var callout = function() {
	$('#system-message').text("Calling remote ...").show();	
};

var call_returned = function() {
	$('#system-message').hide();	
};

var set_customer_data = function(data) {
	call_returned();
	$('#id_town').val(data.town);
	$('#id_address').val(data.address);
	$('#id_phone').val(data.phone);
	$('#id_name').val(data.name);
	$('#id_email').val(data.email);
	$('#id_found_customer_id').val(data.id);

};

var reset_customer_id = function() {
	call_returned();
	$('#id_found_customer_id').val('');
};


var find_customer = function() {
	var postcode = get_normalized_postcode();
	var number = $('#id_number')[0].value
	var addition = $('#id_additions')[0].value

	if (postcode.length === 6) {
		callout();
		$.getJSON('/main/get_customer/' + postcode + '/' + number + '/' + addition, set_customer_data).error(reset_customer_id);
	}
}

var get_normalized_postcode = function() {
	var postcode = $('#id_postcode')[0].value
	return postcode.replace(/ /g, '').toUpperCase();
	
};
$(function() {
	$("#id_postcode").keyup(function(e) {
		var postcode = get_normalized_postcode();
		if (postcode.length === 6) {
			$.getJSON('/pc/get/' + postcode, function(data) {
				$('#id_town').val(data.town);
				$('#id_address').val(data.address);
				$('#id_postcode').val(postcode.toUpperCase());
			});
		}
	});
	$('#id_unrestricted').change(function(e) {
		var unresticted = $('#id_unrestricted').prop('checked');
		if (unresticted === false) {
			clear_data();
		}
		get_updates();
	});
	$("#id_postcode").keyup(function(e) {
		get_updates();
	});
	$("#id_weight").change(function(e) {
		get_updates();
	});
	$("#id_number").keyup(function(e) {
		find_customer();
	});
	$("#id_additions").keyup(function(e) {
		find_customer();
	});
	$("#id_postcode").keyup(function(e) {
		find_customer();
	});
	get_updates();
	$("#id_postcode").focus();
	$('#id_stuff').css('width', '90%')
	$('#id_notes').css('width', '90%')
});
