$(document).ready(function() {

	$('.flash').delay(3000).animate({left: '-200'});
	
	$('.row').mouseover(function() {
		$(this).css('background-color', 'rgba(0, 174, 178, 0.05');
	});

	$('.row').mouseleave(function() {
		$(this).css('background-color', '#fff');
	});

});
