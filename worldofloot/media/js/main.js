$(function() {
  var $handler = $('#pins');
  $handler.imagesLoaded(function() {
    mixpanel.track('images loaded');
    // Pin layout
    $handler.masonry({
      itemSelector: '.pin',
      columnWidth: 269,
      isFitWidth: true
    });

    $('#main-page-loader').hide();
    $('#pins').css('visibility', 'visible');
    // after layout is done, align search, add item, etc. with pins container
    var right_offset = $(window).width() - ($handler.offset().left + $handler.outerWidth());
    $('#user-operations').css('right', Math.min(right_offset, 250));
  });

  $('div .pins a.image-box').fancybox({
    nextClick: true,
    minWidth: 500,
    beforeLoad: function() {
      mixpanel.track('lightbox');
      var el, id = $(this.element).data('title-id');
      if (id) {
        el = $('#' + id);
        if (el.length) {
          this.title = el.html();
        }
      }
    },
    helpers : {
      title : {
        type: 'inside'
      },
      overlay : {
        css : {
          'background' : 'rgba(0, 0, 0, 0.85)'
        }
      },
      thumbs : {
        width: 50,
        height: 50
      }
    }
  });

  $(document).on('click', 'a.js-open-corresponding-lightbox', function() {
    $('#lightbox-trigger-' + $(this).data('lightbox-id')).trigger('click');
    return false;
  });

  var add_modal = new AddItemModal();
  add_modal.Init();

  window.auth_manager = new AuthManager();
  auth_manager.Init();

  window.item_manager = new ItemManager();
  item_manager.Init();

  $('#quick-message-dialog-hide').on('click', function() {
    $('#quick-message-dialog').hide();
    return false;
  });

  $('#items-filter').on('keyup', function() {
    var q = $.trim($(this).val()).toLowerCase();
    if (q == '') {
      $('.pin').show();
      return;
    }

    $('.pin').each(function() {
      if (~$(this).data('item-name').indexOf(q)) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });

  $('#pins').show().css('top', $('#fixed-top-container').height() + 22);

  $('#welcome-close').on('click', function() {
    // close button
    $('#welcome').hide();
    $('#pins').css('top', $('#fixed-top-container').height() + 35);
    $.getJSON('/turn_off_welcome_banner', function() {});
    return false;
  });

  // route
  if (Util.getURLParameter('additem')) {
    // open additem dialog
    mixpanel.track('additem from welcome banner');
    add_modal.ShowModalDialog();
  }
});

function showMessage(msg) {
  var $e = $('#quick-message-dialog');
  $e.find('span').text(msg);
  $e.show();
  setTimeout(function() {
    $e.fadeOut()
  }, 2000);
}
