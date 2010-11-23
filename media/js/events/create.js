var geocoder;
var map;
var locations;
google.maps.event.addDomListener(window, 'load', function() {
	initializeMunichCityCenter();
});

$(function() {
  initialize_location();
  update_location();
	$.datepicker.setDefaults( $.datepicker.regional[ "de" ] );
	$("#id_date_time_begin_0").datepicker( $.datepicker.regional[ "de" ]);
	$("#id_date_time_end_0").datepicker( $.datepicker.regional[ "de" ]);
	$("#id_location").change(update_location);
});

var initialize_location = function() {
    if (locations == null){
        $.getJSON("/events/locations",{id: $(this).val(), ajax: 'true'}, function(jsonLocation){
        locations = new Object();
        var options = '<option value="">- - - - - - - - - -</option>';
        for (var i = 0; i < jsonLocation.length; i++) {
          options += '<option value="' + jsonLocation[i].id + '">' + jsonLocation[i].name + '</option>';
          locations[jsonLocation[i].id] = jsonLocation[i];
        }
        //$("#id_location").html(options);
        update_location();
        });
  }
}

var update_location = function() {
	var id = $("#id_location").val();
	if(id == "") {
		$("#id_location_name")
			.val('')
			.attr('disabled', false);
		$("#id_location_street")
			.val('')
			.attr('disabled', false);
		$("#id_location_city")
			.val('')
			.attr('disabled', false);
	} else if (locations != null) {
		$("#id_location_name")
			.val(locations[id].name)
			.attr('disabled', true);
		$("#id_location_street")
			.val(locations[id].street)
			.attr('disabled', true);
		$("#id_location_city")
			.val(locations[id].city)
			.attr('disabled', true);
		$("#id_location_show_in_map").click();
	}
};

