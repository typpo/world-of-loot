function ScrollManager() {
  var me = this;

  var isLoading = false;  // always false for now
  function onScroll(event) {
    // Only check when we're not still waiting for data.
    if(!isLoading) {
      // Check if we're within 100 pixels of the bottom edge of the broser window.
      var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
      if(closeToBottom) {
        loadData();
      }
    }
  }

  function loadData() {
    // Load in the next bunch
    var $newpins = $('#pins .pin-hidden:lt(10)').css('visibility', 'hidden').show();
    // TODO set images to load
    // TODO show loader
    $newpins.imagesLoaded(function() {
      $newpins.removeClass('pin-hidden').addClass('pin').each(function() {
        var $pinimg = $(this).find('img');
        $pinimg.attr('src', $pinimg.data('src'));
      });
      $('#pins').masonry('appended', $newpins, true);
      $newpins.css('visibility', 'visible');
    })
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
    $(document).bind('scroll', onScroll);
    window.sm = me;
  }

  this.TriggerLoad = function() {
    loadData();

  }
}
