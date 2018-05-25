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

/**
 * Configure Javascript to hide/show Google Analytics and comply with GPDR
 * requirements on tracking disclosure.
 */
$(document).ready(function() {

  // Get the opt-in toggle for functons and default to hiding alert
  var $optinToggle = $('#analytics-optin');
  $('.alert').hide();


  // bind cookie expiry and setting + rendering GA to the toggle checkboxs
  $optinToggle.change(function() {
    if (this.checked) {
      renderGA();
    } else {
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('event', 'opt-out', {
        'event_category': 'GPDR',
        'event_label': getClientID()
      });
      Cookies.expire('pliny_analytics_optin');
      Cookies.expire('_gat_gtag_UA_104408652_1');
      Cookies.expire('_ga');
      Cookies.expire('_gid');

    }
  });

  // Bind closing alert to click for opening modal to review cookie policy
  $('#close-priv-alert').click(function() {
      $('.alert').alert('close');
  });

  /**
   * Check whether the opt in cookie exists. If it does, mark the check box
   * to indicate this fact, otherwise see if we're in an EU country.
   */
  function checkOptInCookie() {
    var optin = Cookies.get('pliny_analytics_optin');
    if (optin == undefined ) {
      getCountry();
    }
    if (optin === 'true') {
      $optinToggle.prop('checked', true);
      renderGA();
    }
  }


  /**
   * Set the pliny_analytics cookie for 90 days
   */
  function setCookie() {
    var expiry = new Date();
    expiry.setDate(expiry.getDate() + 90)
    Cookies.set('pliny_analytics_optin', 'true',
      {'expires': expiry.toUTCString()});
    // This is an opt in, so we
  }

  function getClientID() {
    return Cookies.get('_ga').replace(/GA\d\.\d./g, "");
  }

  /**
   * Render Google Analytics and do an ajax GEY of the script
   */
  function renderGA() {
    $.getScript("https://www.googletagmanager.com/gtag/js?id=UA-104408652-1", function() {
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'UA-104408652-1', { 'anonymize_ip': true });

      if (Cookies.get('pliny_analytics_optin') === undefined) {
        setCookie();
        gtag('event', 'opt-in', {
          'event_category': 'GPDR',
          'event_label': getClientID(),
        });
      }
    });
  }

  /**
   * Do a lookup using the url to local API. Ajax call returns a country code
   * and sets GA if a non-EU country by default.
   */
  function getCountry() {
    $.ajax({
      url: $('#country-lookup').text(),
      success: function(data) {
        euMembers = ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES',
          'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT',
          'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'UK']
        if ($.inArray(data, euMembers) == -1 && data !== '') {
          $optinToggle.prop('checked', true);
          renderGA();
        } else {
          $('.alert').fadeIn(800);
        }
      }
    });
  }

  // Initializes the callbacks that configure GA.
  checkOptInCookie();

});


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
