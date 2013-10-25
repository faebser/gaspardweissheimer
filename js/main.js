
var gaspi = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		win = $(window),
		main = $('#main'),
		navElements = main.find('li'),
		tops = $('.top'),
		verticalNav = $('#verticalNav'),
		topElementsToSwitchColor = $('nav li a, #logo'),
		topElementsToSwitchBack = $("#indicator"),
		bullets = {
			"active" : "&bull;",
			"inactive" : "&#9702;" 
		};
	// private methods
	var init = function () {
		var winHeight = parseInt(win.height());
		tops.height(winHeight);
		verticalNavInit(winHeight);
		clickHandlers(winHeight);

	},
	verticalNavInit = function (winHeight) {
		var length = navElements.length,
			ul = verticalNav.find('ul'),
			width = 0,
			scrollingAmount = 100 / length;

		for(var i = 0; i < length; i++) {
			var bullet = bullets.inactive;
			if(i == 0) {
				bullet = bullets.active;
			}
			var li = $('<li/>').html(bullet);
			li.data({
				"scroll" : scrollingAmount * i,
				"color" : navElements.eq(i).attr("class")
			});
			ul.append(li);
			li.click(function () {
				main.transition({
					'x' : $(this).data("scroll") * -1 + "%"
				}, 1500, 'snap');
				// TODO recode this shit & init
				var color = "";
				if (typeof $(this).data("color") === 'undefined') {
					color = "#000"
				}
				else {
					color = $(this).data("color");
				};
				topElementsToSwitchColor.css({
					"color" : color
				});
				topElementsToSwitchBack.css({
					"background-color" : color
				});
				return;
			});
			width += parseInt(li.width());
		}
		ul.css({
			"width" : width
		});
		verticalNav.css({
			"top" : winHeight - 150
		});
	},
	clickHandlers = function (winHeight) {
		win.scroll(function(event) {
			console.log(win.scrollTop() / winHeight);
			tops.css({
				"opacity" : 1 - win.scrollTop() / winHeight 
			})
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