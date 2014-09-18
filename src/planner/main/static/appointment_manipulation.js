/* global  globalCalendarId:false, globalDateIso:false, $:false, window:false,  clearData:false, getUpdates:false, getUpdates_unrestricted:false */

'use strict';

var showPostCodeDotNlWindow = false;

var calloutAvailableDates = function() {
  $('#date-search').show();	
};
var calloutKnownCustomers = function() {
  $('#customer-search').show();	
};
var calloutPostcode = function() {
  $('#postcode-search').show();	
};

var callReturnedAvailableDates = function() {
  $('#date-search').hide();	
};
var call_returned_known_customers = function() {
  $('#customer-search').hide();	
};
var call_returned_postcode = function() {
  $('#postcode-search').hide();	
};

var setCustomerData = function(data) {
  call_returned_known_customers();
  if (data.found === true) {
    $('#id_town').val(data.town);
    $('#id_address').val(data.address);
    $('#id_phone').val(data.phone);
    $('#id_name').val(data.name);
    $('#id_email').val(data.email);
    $('#id_found_customer_id').val(data.id);
    window.customer_answers.push(data.id);
  } else {
    reset_customer_id();
  } 
};

var get_carId = function() {
  var id = $('#id_car').val();
  if (id === '') {
    id = '-1';
  }
  return id;
};

var reset_customer_id = function() {
  $('#id_found_customer_id').val('');
  window.customer_answers.push('RESET');
};


var findCustomer = function() {
  var postcode = get_normalized_postcode();
  var number = $('#id_number')[0].value;
  var addition = $('#id_additions')[0].value;

  if (postcode.length === 6) {
    calloutKnownCustomers();
    $.getJSON('/main/get_customer/' + postcode + '/' + number + '/' + addition, setCustomerData).error(reset_customer_id);
  }
};

var get_normalized_postcode = function() {
  var postcode = $('#id_postcode')[0].value;
  return postcode.replace(/ /g, '').toUpperCase();

};
$(function() {
  $('#car_choice').hide();
  window.customer_answers = [];
  $('#id_postcode').keyup(function() {
    var postcode = get_normalized_postcode();
    if (postcode.length === 6) {
      calloutPostcode();
      $.getJSON('/pc/get/' + postcode, function(data) {
        call_returned_postcode();
        if (data.found === true) {
          $('#id_town').val(data.town);
          $('#id_address').val(data.address);
          $('#id_postcode').val(postcode.toUpperCase());
        } else {
          if (!showPostCodeDotNlWindow) {
            showPostCodeDotNlWindow = true;
            window.open('http://postcode.nl/zoek/'+ postcode);
          }
        }
      }).error( 
        function(error) {
          call_returned_postcode();
        });
    }
  });
  var getUpdatesConditional = function() {
    var unresticted = $('#id_unrestricted').prop('checked');
    if (unresticted === false) {
      clearData();
      getUpdates();
    } else {
      getUpdates_unrestricted();			
    }
  };
  $('#id_unrestricted').change(function() {
    getUpdatesConditional();
  });
  $('#id_kind').change(function() {
    var kind = $('#id_kind')[0].value;
    if (kind === '1') {
      $('#id_unrestricted').prop('checked', true);
      $('#car_choice').show();
    } else {
      $('#id_car').val('');
      $('#car_choice').hide();
    }
    getUpdatesConditional();
  });
  $('#id_car').change(function() {
    getUpdatesConditional();
  });
  $('#id_postcode').keyup(function() {
    getUpdates();
  });
  $('#id_weight').change(function() {
    getUpdates();
  });
  $('#id_number').keyup(function() {
    findCustomer();
  });
  $('#id_additions').keyup(function() {
    findCustomer();
  });
  $('#id_postcode').keyup(function() {
    findCustomer();
  });
  getUpdates();
  $('#id_postcode').focus();
  $('#id_stuff').css('width', '90%');
  $('#id_notes').css('width', '90%');
});

var on_click = function(calendarId) {
  return function(e) {
    if(e.ctrlKey) {
      window.open('/main/list/appointments/' + calendarId);
    }
  };

}
var set_data = function(data) {
  callReturnedAvailableDates();
  $('#region_label').text(data.region);
  $('#id_free_space').empty();
  for (var i = 0, len = data.dates.length; i < len; i++) {
    var date = data.dates[i];
    var calendarId = date[0];
    var option;
    if (globalCalendarId == calendarId) {
      option = '<option id="' + calendarId + '" selected="selected" value="' + calendarId + '">' +  date[1] + '</option>';
    } else {
      option = '<option id="' + calendarId + '" value="' + calendarId + '">' +  date[1] + '</option>';
    }
    $('#id_free_space').append(option);
    $('#' + calendarId).click(on_click(calendarId));

  }

};
var clearData = function() {
  var unresticted = $('#id_unrestricted').prop('checked');
  callReturnedAvailableDates();
  if (unresticted === false) {
    $('#id_free_space').empty();
  }
};
var getUpdates = function() {
  var postcodeToSend;
  var postcode = get_normalized_postcode();
  var unrestricted = $('#id_unrestricted').prop('checked');
  var carId = "-1";
  if (unrestricted) {
    postcodeToSend = "-1";
    carId = get_carId();
  } else {
    postcodeToSend = postcode;
  }

  var weight = $('#id_weight')[0].value;
  var kind = $('#id_kind')[0].value;
  var url = '/main/get_candidate_dates/' + globalDateIso +'/' + weight + '/' + postcodeToSend + '/' + carId + '/' + kind + '/' + globalCalendarId;
  if (postcode.length === 6) {
    calloutAvailableDates();
    $.getJSON(url, set_data).error(clearData);
  }
};
var getUpdates_unrestricted = function() {
  var postcodeToSend;
  var postcode = get_normalized_postcode();
  var unrestricted = $('#id_unrestricted').prop('checked');
  var carId = '-1';
  if (unrestricted) {
    postcodeToSend = '-1';
    carId = get_carId();
  } else {
    postcodeToSend = postcode;
  }
  var weight = $('#id_weight')[0].value;
  var kind = $('#id_kind')[0].value;
  var url;
  if (unrestricted === true) {
    var url = '/main/get_candidate_dates/' + globalDateIso +'/' + weight + '/' + postcodeToSend + '/' + carId + '/' + kind + '/' + globalCalendarId;
    calloutAvailableDates();
    $.getJSON(url, set_data).error(clearData);
  }
};

