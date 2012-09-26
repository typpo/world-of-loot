;function ItemManager() {
  var me = this;

  this.Init = function() {

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
