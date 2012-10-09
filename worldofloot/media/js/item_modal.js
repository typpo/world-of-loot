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

    // Submit button
    $('#add-item button.btn-add-item').on('click', function() {
      mixpanel.track('add item', {
        id: me.id,
        type: me.type
      });

      $(this).addClass('disabled');
      me.AddItem(me.id, me.type, 'want', $('#add-item-comment').val(), function(err, data) {
        if (err) {
          return;
        }
        $('#add-item').modal('hide');
        item_manager.AddItemToPage(data.pin_html);
      });
    });

    // Show modal dialog
    $(document).on('click', 'a.js-add-pin, button.js-add-pin', function() {
      mixpanel.track('add pin modal', {
        from: $(this).attr('id')
      });
      me.ShowModalDialog();
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

  this.ShowModalDialog = function() {
    $('#add-item-image-container').empty();
    $('#add-item').modal();
    $('#add-item-id').val('').focus()
  }
}


