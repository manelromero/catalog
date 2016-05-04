$(document).ready(function() {

	$('.row').mouseover(function() {
		$(this).css('background-color', '#eee');
	});

	$('.row').mouseleave(function() {
		$(this).css('background-color', '#fff');
	});

	$('.flash').click(function() {
		$(this).css('display', 'none');
	});

});
