$(document).ready(function(){
    $('#capture-btn').click(function(){
      $.post('/capture', {img: $('#video').attr('src')}, function(data){
        var html = '<h2>Image Captured:</h2>';
        html += '<img src="' + data + '">';
        $('#capture-container').html(html);
      });
    });
  });
  