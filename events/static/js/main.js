$(document).ready(function() {

	$('.flash').delay(2000).slideUp(300);
	$('.flash').click(function() {
		$(this).slideUp(300);
	});

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
