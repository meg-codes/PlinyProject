/**
 * Lookup people to populate existing doughnut chart
*/
var lookupPeople = function() {

}
/**
 * Function to render a doughnut chart of correspondents' social classes
 * and to bind update AJAX calls to a simple select form.
*/
function renderDonutChart() {

  // Get the jQuery object for the html5 canvas
  var donutChart = $("#donut-chart");

  // Append options to the form to avoid hardcoding it all in the template
  // not necessary but less code.
  $('#book-select').append($('<option />').val('').text('All'));
  for (var i = 1; i < 10; i++) {
    $('#book-select').append($('<option />').val(i).text(i));
  }

  // Perform an AJAX call to render initial values and render the form.
  $.ajax({
    url: "/people/social_class.json",
    success: function(data) {
      var classDonutChart = new Chart(donutChart, {
        type: 'doughnut',
        data: data,
      })
    }
  });

  // Bind a callback to picking a book from dropdown to update chart
  $('#book-select').change(function() {
    $.ajax({
      url: "/people/social_class.json",
      data: {q: $(this).val()},
      success: function(data) {
        classDonutChart.data = data;
        classDonutChart.update();
      }
    });
  });

}
