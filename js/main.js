$(document).ready(function(){

  $('.ir-arriba').click(function(){
      $('body, html').animate({
          scrollTop: '0px'
      }, 1000);
  });

  $(window).scroll(function(){
      if( $(this).scrollTop() > 0 ){
          $('.ir-arriba').slideDown(700);
      } else {
          $('.ir-arriba').slideUp(700);
      }
  });

  var tag = document.createElement('script');

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
  
  var player;
  function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
      videoId: '5DQnIbL3g3Y',
      events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
      }
    });
  }
  
  function onPlayerReady(event) {
    event.target.playVideo();
  }
  
  var done = false;
  function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
      setTimeout(stopVideo, 6000);
      done = true;
    }
  }
  function stopVideo() {
    player.stopVideo();
  }

});

