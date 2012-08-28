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
});
