function ScrollManager() {
  var me = this;

  var page = 1;
  var loaderEnabled = true;
  var lastLoaded = new Date().getTime();

  function onScroll(event) {
    // Check if we're within 200 pixels of the bottom edge of the browser window.
    var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 800);
    var now = new Date().getTime();
    if(closeToBottom && now - lastLoaded > 300) {
      loadData();
      lastLoaded = now;
    }
  }

  function loadData() {
    if (!loaderEnabled) return;
    $('#pagination').css('visibility', 'hidden');

    $('#more-pins-loader').show('fast');

    loaderEnabled = false;
    $.getJSON('/api/' + wol_tab_context + '/' + page, function(data) {
      loaderEnabled = true;
      $('#more-pins-loader').hide('fast');
      if (!data || !data.pin_html || !data.success) {
        // nothing more (or an error occurred)
        return;
      }
      var $newpins = $(data.pin_html).css('visibility', 'hidden')
        .appendTo('#pins').imagesLoaded(function() {
          $('#pins').masonry('appended', $newpins, true);
          $newpins.css('visibility', 'visible');
          mixpanel.track('scrolled');
      });
      page++;
    });
  }

  function initialLoadData() {
    // Image layout
    var $handler = $('#pins');
    $handler.imagesLoaded(function() {
      mixpanel.track('images loaded');
      // Pin layout
      $handler.masonry({
        itemSelector: '.pin',
        columnWidth: 269,
        isFitWidth: true,
        isAnimated: !Modernizr.csstransitions
      });

      $('#main-page-loader').hide();
      $('#pins').css('visibility', 'visible');
      // after layout is done, align search, add item, etc. with pins container
      var right_offset = $(window).width() - ($handler.offset().left + $handler.outerWidth());
      $('#user-operations').css('right', Math.min(right_offset, 250));
    });

  }

  this.Init = function() {
    initialLoadData();
    // hack so always scrollable
    $('body').css('height', $(window).height() + 10);
    $(document).bind('scroll', onScroll);
    window.sm = me;
  }

  this.TriggerLoad = function() {
    loadData();

  }
}
