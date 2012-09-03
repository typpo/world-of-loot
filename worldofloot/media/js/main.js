function AddItemModal() {
  this.Init = function() {
    var me = this;
    $('#add-item-id').on('change', function() {
      var id = $.trim($(this).val());
      if (id === '') return;
      $('#add-item-loader').show();
      $.getJSON('/info/' + id, function(data) {
        $('#add-item-loader').hide();
        if (!data || !data.images) {
          alert("Sorry, I couldn't find this item.  Please try something different.");
          return;
        }

        $('#add-item-image-container').html('<a href="#" rel="item=' + id + '"><h3>' + data.name + '</h3><img src="' + data.images[0] + '"/></a>');

        $('#add-item button').removeClass('disabled');
        me.id = id;
      });
    });

    $('#add-item button.btn-add-item').on('click', function() {
      // TODO some sort of loader
      $.get('/add/' + me.id, function(data) {

        $('#add-item').modal('hide');
        window.location.reload();
      }, 'json');
    });

    // Show modal dialog
    $('a.js-add-pin').on('click', function() {
      $('#add-item').modal();
      $('#add-item-id').focus()
    });
  }
}

$(function() {
  var $handler = $('#pins .pin');
  $handler.imagesLoaded(function() {
    $handler.wookmark({
      offset: 10,
      itemWidth: 250,
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
});
