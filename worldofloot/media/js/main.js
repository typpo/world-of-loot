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
      me.AddItem(me.id, me.type, 'want', function(err, success) {
        if (err) {
          return;
        }
        $('#add-item').modal('hide');
        // TODO maybe don't reload because it resets scrolling
        window.location.reload();
      });
    });

    // Show modal dialog
    $('a.js-add-pin').on('click', function() {
      $('#add-item-image-container').empty();
      $('#add-item').modal();
      $('#add-item-id').val('').focus()
    });

    // Pin deletion
    $('.delete-pin').on('click', function() {
      var type = $(this).data('item-type');
      var id = $(this).data('item-id');
      $.getJSON('/remove/' + type + '/' + id, function(data) {
        window.location.reload();
      });
    });

    // Wants
    $('.js-item-want').on('click', function() {
      me.AddItem($(this).data('item-id'), $(this).data('item-type'),
        'want', function(err, success) {
        if (err) {
          alert("You already did this!");
          return;
        }
        window.location.reload();  // TODO maybe no refresh
      });
    });

    // Haves
    $('.js-item-have').on('click', function() {
      me.AddItem($(this).data('item-id'), $(this).data('item-type'),
        'have', function(err, success) {
        if (err) {
          alert("You already did this!");
          return;
        }
        window.location.reload();  // TODO maybe no refresh
      });
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

      $('#add-item-image-container').html('<a href="#" rel="'
        + type + '=' + id + '"><h3>' + data.name
        + '</h3><img src="' + data.images[0] + '"/></a>');

      $('#add-item button').removeClass('disabled');
      me.id = id;
      me.type = type;
      me.loaded_image = true;
    });
  }

  this.AddItem = function(id, type, verb, callback) {
    // TODO this belongs in a general function, not just additemmodal
    // TODO some sort of loader
    $.get('/add/' + type + '/' + id + '/' + verb, function(data) {
      if (data.already_have) {
        callback(true, null);
      }
      else {
        callback(null, true);
      }
    }, 'json');
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
  var $handler = $('#pins .pin');
  $handler.imagesLoaded(function() {
    $handler.wookmark({
      offset: 10,
      itemWidth: 260,
      autoResize: true,
    });
    /*
    $handler.masonry({
      itemSelector: '.pin',
      columnWidth: 300,
    });
    */
  });

  var add_modal = new AddItemModal();
  add_modal.Init();

  window.auth_manager = new AuthManager();
  auth_manager.Init();
});
