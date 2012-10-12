;function ItemManager() {
  var me = this;

  this.Init = function() {
    // Pin deletion
    $(document).on('click', '.delete-pin', function() {
      // TODO all this should go in itemmanager
      mixpanel.track('delete pin');
      var $e = $(this);
      var type = $e.data('item-type');
      var id = $e.data('item-id');
      $.getJSON('/remove/' + type + '/' + id, function(data) {
        //window.location.reload();
        item_manager.RemoveItemFromPage($e.parent());
      });
      return false;
    });

    // Wants
    $(document).on('click', '.js-item-want', function() {
      mixpanel.track('item want');
      var comment = ''; //prompt("Add a comment (or leave it blank)");
      var item_id = $(this).data('item-id');
      var item_type = $(this).data('item-type');
      add_modal.AddItem(item_id, item_type,
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
      mixpanel.track('item have');
      var comment = ''; //prompt("Add a comment (or leave it blank)");
      var item_id = $(this).data('item-id');
      var item_type = $(this).data('item-type');
      add_modal.AddItem(item_id, item_type,
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

  this.AddItemToPage = function(pin_html) {
    // TODO make me!
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
