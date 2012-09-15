function AddItemModal() {
  this.Init = function() {
    var me = this;

    // Autocomplete
    $("#add-item-id").autocomplete({
      minLength: 2,
      source: function(request, response) {
        $.getJSON('/autocomplete/' + request.term, function(data) {
          var arr = [];
          for (var i=0; i < data.length; i++) {
            arr.push({data: data[i],
              label: data[i].name, value: data[i].name});
          }
          response(arr);
        });
      },
      select: function(event, ui) {
        if (ui.item) {
          me.LoadImage(ui.item.data.id, ui.item.data.type);
        }
      }
    // TODO format to use data[i].name
    });

    $('#add-item-id').on('keydown', function(e) {
      var $submit = $('#add-item button.btn-add-item');
      if (e.keyCode == 13 && !$submit.hasClass('disabled')) {
        $submit.click();
      }
    });

    // Submit button
    $('#add-item button.btn-add-item').on('click', function() {
      me.AddItem(me.id, me.type, 'want', $('#add-item-comment').val(), function(err, data) {
        if (err) {
          return;
        }
        $('#add-item').modal('hide');
        // TODO maybe don't reload because it resets scrolling
        //window.location.reload();
        console.log('calling additem');
        item_manager.AddItemToPage(data.pin_html);
      });
    });

    // Show modal dialog
    $(document).on('click', 'a.js-add-pin, button.js-add-pin', function() {
      $('#add-item-image-container').empty();
      $('#add-item').modal();
      $('#add-item-id').val('').focus()
      return false;
    });

    // Pin deletion
    $(document).on('click', '.delete-pin', function() {
      // TODO all this should go in itemmanager
      var $e = $(this);
      var type = $e.data('item-type');
      var id = $e.data('item-id');
      $.getJSON('/remove/' + type + '/' + id, function(data) {
        //window.location.reload();
        item_manager.RemoveItemFromPage($e.parent());

      });
    });

    // Wants
    $(document).on('click', '.js-item-want', function() {
      var comment = prompt("Add a comment (or leave it blank)");
      var item_id = $(this).data('item-id');
      var item_type = $(this).data('item-type');
      me.AddItem(item_id, item_type,
        'want', comment, function(err, success) {
        if (err) {
          showMessage("You already added this!");
          return;
        }
        showMessage("This item has been added to your wishlist.");
        // increment counter
        var $wants_count = $('span.' + item_id + '-' + item_type + '-wants-count');
        $wants_count.html(parseInt($wants_count.html(), 10)+1);
      });
      return false;
    });

    // Haves
    $(document).on('click', '.js-item-have', function() {
      var comment = prompt("Add a comment (or leave it blank)");
      var item_id = $(this).data('item-id');
      var item_type = $(this).data('item-type');
      me.AddItem(item_id, item_type,
        'have', comment, function(err, success) {
        if (err) {
          showMessage("You already added this!");
          return;
        }
        showMessage("This item has been added to your loot.");
        // increment counter
        var $haves_count = $('span.' + item_id + '-' + item_type + '-haves-count');
        $haves_count.html(parseInt($haves_count.html(), 10)+1);
      });
      return false;
    });
  }

  this.LoadImage = function(id, type) {
    // Loads image after user selection
    var me = this;
    me.loaded_image = false;
    $('#add-item-loader').show();
    $.getJSON('/info/' + type + '/' + id, function(data) {
      $('#add-item-loader').hide();
      if (!data || !data.images) {
        alert("Sorry, I couldn't find this item.  Please try something different.");
        return;
      }

      var imgpath = data.images.length > 0 ? data.images[0] : '/media/images/unavailable.png';
      $('#add-item-image-container').html('<a href="#" rel="'
        + type + '=' + id + '"><h3>' + data.name
        + '</h3><img src="' + imgpath + '"/></a>');

      $('#add-item button').removeClass('disabled');
      me.id = id;
      me.type = type;
      me.loaded_image = true;
    });
  }

  this.AddItem = function(id, type, verb, comment, callback) {
    // TODO turn into options
    // TODO this belongs in a general function, not just additemmodal
    // TODO some sort of loader
    $.post('/add/' + type + '/' + id + '/' + verb, {
      comment: comment
    }, function(data) {
      if (data.already_have) {
        callback(true, null);
      }
      else {
        callback(null, data);
      }
    }, 'json');
  }
}

function ItemManager() {
  var me = this;

  this.Init = function() {

  }

  this.AddItemToPage = function(pin_html) {
    // TODO make me!
    //console.log('anus', pin_html);
    $('#pins').append(pin_html);
    var $pin = $(pin_html);
    $('#pins').append($pin).masonry('appended', $pin);
    $('#pins .pin').not('.masonry-brick').remove();
  }

  this.RemoveItemFromPage = function($e) {
    $e.remove();
    $('#pins').masonry('reload');
  }
}

function AuthManager() {
  this.Init = function() {
    var me = this;

    // csrf stuff
    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }
    });

    // Login/register button
    $('#login-register-modal a.submit').on('click', function() {
      me.Login(
        $('#login-register-username').val(),
        $('#login-register-password').val(),
        $('#login-register-remember-me').prop('checked') ? true : false
      );
      return false;
    });

    // Show modal
    $('a.js-login').on('click', function() {
      me.ShowLogin();
      return false;
    });
  }

  this.ShowLogin = function() {
    $('#login-register-modal').modal();
    $('#login-register-username').focus();
  }

  this.Login = function(username, password, remember) {
    $.post('/login_or_create/', {
      username: username,
      password: password,
      remember_me: remember
    }, function(data) {
      if (data && data.success)
        window.location.reload()
      else
        alert('Login failed.  Reason: ' + data.reason);
    }, 'json');
  }
}

$(function() {
  var $handler = $('#pins');
  $handler.imagesLoaded(function() {
    // Pin layout
    /*
    $handler.wookmark({
      offset: 10,
      itemWidth: 260,
      autoResize: true,
    });
    */

    $handler.masonry({
      itemSelector: '.pin',
      columnWidth: 269,
      isFitWidth: true,
    });

    $('#main-page-loader').hide();
    $('#pins').css('visibility', 'visible');
    // after layout is done, align search, add item, etc. with pins container
    var right_offset = $(window).width() - ($handler.offset().left + $handler.outerWidth());
    $('#user-operations').css('right', Math.min(right_offset, 250));
  });

  $('div .pins a.image-box').fancybox({
    nextClick: true,
    midWidth: 500,
    beforeLoad: function() {
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
});

function showMessage(msg) {
  var $e = $('#quick-message-dialog');
  $e.find('span').text(msg);
  $e.show();
  setTimeout(function() {
    $e.fadeOut()
  }, 2000);
}
