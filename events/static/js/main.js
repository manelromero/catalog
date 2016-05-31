$(document).ready(function() {

	$('.flash').delay(3000).animate({left: '-200'});
	
	$('.row').mouseover(function() {
		$(this).css('background-color', 'rgba(0, 174, 178, 0.05');
	});

	$('.row').mouseleave(function() {
		$(this).css('background-color', '#fff');
	});

	$('.members').on('mouseover', '.member', function() {
		$(this).css('background-color', 'rgba(0, 174, 178, 0.05');
	});

	$('.members').on('mouseleave', '.member', function() {
		$(this).css('background-color', '#f5f5f5');
	});

	$('.unfold').click(function() {
		var id = $(this).data('id');
		$.ajax({
			url: '/show-category-members/' + id,
			async: false,
			success: function(data) {
				$('[data-category=' + id + ']').html(data);
			}
		});
		$(this).toggleClass('more');
		$('[data-category=' + id + ']').slideToggle(300);
	});

});
