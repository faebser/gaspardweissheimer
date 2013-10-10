
var gaspi = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		win = $(window),
		tops = $('.top'),
		main = $('#main'),
		verticalNav = $('#verticalNav'),
		bullets = {
			"active" : "&bull;",
			"inactive" : "&#9702;" 
		};
	// private methods
	var init = function () {
		var winHeight = parseInt(win.height());
		tops.height(winHeight);
		verticalNavInit(winHeight);

	},
	verticalNavInit = function (winHeight) {
		var length = tops.length,
			ul = verticalNav.find('ul'),
			width = 0,
			scrollingAmount = 100 / length;
		for(var i = 0; i < length; i++) {
			var bullet = bullets.inactive;
			if(i == 0) {
				bullet = bullets.active;
			}
			var li = $('<li/>').html(bullet);
			ul.append(li);
			console.log(i * scrollingAmount);
			li.data("scroll", i * scrollingAmount);
			li.click(function () {
				console.log($(this).data('scroll') * -1 + "%");
				main.transition({
					'x' : $(this).data("scroll") * -1 + "%"
				}, 1000, 'snap');
			});
			width += parseInt(li.width());
		}
		ul.css({
			"width" : width
		});
		verticalNav.css({
			"top" : winHeight - 150
		});
	};
	// public methods
	module.init = function () {
		init();
	};
	//return the module
	return module;
}(jQuery));

jQuery(document).ready(function($) {
	gaspi.init();
});