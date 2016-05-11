$(document).ready(function() {

	$('.row').mouseover(function() {
		$(this).css('background-color', 'rgba(0, 174, 178, 0.05');
	});

	$('.row').mouseleave(function() {
		$(this).css('background-color', '#fff');
	});

	$('.flash').click(function() {
		$(this).hide(500);
	});

});
