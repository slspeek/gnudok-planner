"use strict";

var callout_available_dates = function() {
	$('#date-search').show();	
};
var callout_known_customers = function() {
	$('#customer-search').show();	
};
var callout_postcode = function() {
	$('#postcode-search').show();	
};

var call_returned_available_dates = function() {
	$('#date-search').hide();	
};
var call_returned_known_customers = function() {
	$('#customer-search').hide();	
};
var call_returned_postcode = function() {
	$('#postcode-search').hide();	
};

var set_customer_data = function(data) {
	call_returned_known_customers();
	$('#id_town').val(data.town);
	$('#id_address').val(data.address);
	$('#id_phone').val(data.phone);
	$('#id_name').val(data.name);
	$('#id_email').val(data.email);
	$('#id_found_customer_id').val(data.id);

};

var get_car_id = function() {
	var id = $('#id_car').val();
	if (id === "") {
		id = "-1";
	}
	return id;
}

var get_car_name = function() {
	var name = $('#id_car option:selected').text();
	return name;
}

var reset_customer_id = function() {
	call_returned_known_customers();
	$('#id_found_customer_id').val('');
};


var find_customer = function() {
	var postcode = get_normalized_postcode();
	var number = $('#id_number')[0].value;
	var addition = $('#id_additions')[0].value;

	if (postcode.length === 6) {
		callout_known_customers();
		$.getJSON('/main/get_customer/' + postcode + '/' + number + '/' + addition, set_customer_data).error(reset_customer_id);
	}
}

var get_normalized_postcode = function() {
	var postcode = $('#id_postcode')[0].value;
	return postcode.replace(/ /g, '').toUpperCase();
	
};
$(function() {
	$('#id_car').hide();
	$("#id_postcode").keyup(function(e) {
		var postcode = get_normalized_postcode();
		if (postcode.length === 6) {
			callout_postcode();
			$.getJSON('/pc/get/' + postcode, function(data) {
				call_returned_postcode();
				$('#id_town').val(data.town);
				$('#id_address').val(data.address);
				$('#id_postcode').val(postcode.toUpperCase());
			}).error( 
			function(error) {
				call_returned_postcode();
			});
		}
	});
	var get_updates_conditional = function() {
		var unresticted = $('#id_unrestricted').prop('checked');
		if (unresticted === false) {
			clear_data();
			get_updates();
		} else {
			get_updates_unrestricted();			
		}
	}
	$('#id_unrestricted').change(function(e) {
		get_updates_conditional();
	});
	$('#id_kind').change(function(e) {
		var kind = $('#id_kind')[0].value
		if (kind === "1") {
			$('#id_unrestricted').prop('checked', true);
			$('#id_car').show();
		} else {
			$('#id_car').val('');
			$('#id_car').hide();
		}
		get_updates_conditional();
	});
	$('#id_car').change(function(e) {
		get_updates_conditional();
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
	$('#id_stuff').css('width', '90%');
	$('#id_notes').css('width', '90%');
});
