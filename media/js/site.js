/**
 * Obscure email addresses via Javascript by replacing (at) with @
 * @param value - a string to replace (at) with @
 */
function removeObfus(value) {
    // Snip from https://gist.github.com/mathiasbynens/28682
    // adapted for use
    return value.replace('(at)', '@').replace(/\(dot\)/g, '.');
}

/**
 * Perform an person name query using a jQuery ajax call.
 * @param request - the autocomplete request
 * @param response - a callback function to operate on the data
 */
function getAutocomplete(request, response) {
    var query = request.term;
    $.ajax("/people/autocomplete/", {
      data: {q: query},
      success: function(data) {
        return response(data);
      },
      always: function() {
        return response()
      }
    });
}

$(document).ready(function() {

    // Initialize the
    $("#nav_nomina").autocomplete({
      source: getAutocomplete,
      classes: {
        "ui-autocomplete": "ui-front"
      },
      appendTo: $('nav')
    });


     $('a[href^="mailto:"]').each(function() {
      this.href = removeObfus(this.href);
     });


  });
