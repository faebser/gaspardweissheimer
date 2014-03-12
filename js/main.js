var loader = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		images = {},
		smallOffset = $(window).height() - 20,
		selector = 'img.ajax',
		body = $('body'),
		doc = $(document),
		main = $('#main'),
		loaded = 'loaded',
		next = 0,
		activeParentId = false,
		c = {
			'home': 'home',
			'page': 'page',
			'notLoaded': 'notLoaded'
		}
	// private methods
	var check = function () {
		if (activeParentId) {
			var scrollOffset = doc.scrollTop(); // maybe implement next?
			console.log("balabala called at: " + scrollOffset);
			if(next === 0) { // setup check
				setupCheck();
			}
			// check
			if(scrollOffset >= next) { // we hit an image
				runImage(images[activeParentId][0]);
				// run again, just in case we scrolled alot
				setupCheck();
				check();
			}
		};
	},
	setupCheck = function () { // maybe make this smart?
		next = images[activeParentId][0].offset; // error when array empty
	},
	runImage = function (image) {
		var e = image.element;
		e.attr('src', e.data('src')).imagesLoaded(function (instance) {
			console.log(e);
			console.log(this);
			console.log("loaded");
			console.log(instance);
			e.removeClass(c.notLoaded);
		});
		images[activeParentId].splice(0, 1);
		console.log(images[activeParentId]);
	},
	addImage = function (el, parent) {
		var id = parent.attr('id');
		if(!images.hasOwnProperty(id)) {
			images[id] = [];
		}
		images[id].push({
			'offset' : el.position().top - smallOffset,
			'element' : el
		});
	};
	// public methods
	module.checkForImages = function(parent) {
		parent.find('li').each(function(index, parent) {
			var p = $(parent);
			p.find(selector).each(function(cIndex, el){
				var e = $(el);
				addImage(e, p);
				e.css('height', e.height()).data('src', e.attr('src')).attr('src', '').addClass(c.notLoaded); // the height is the same for all images
			});
			// images.push(e.offset().top - smallOffset);
			// images[e.offset().top - smallOffset] = e;
			// e.hide().attr('src', '');
			return;
		});
		console.log(images);
		$(document).on('scroll', check);
	},
	module.reset = function() {
		images.clear();
		$(document).off('scroll', check);
	},
	module.setActiveParent = function (parentID) {
		activeParentId = parentID;
	},
	module.init = function () {
		if(body.attr('id') === c.home) {
			module.checkForImages(main);
		}
	};
	//return the module
	return module;
}(jQuery));

var gaspi = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		win = $(window),
		body = $("body"),
		main = $('#main'),
		navElements = main.find('li'),
		tops = $('.top'),
		verticalNav = $('#verticalNav'),
		scrollIndicator = $('#scrollIndicator'),
		topElementsToSwitchColor = $('nav li a, #logo'),
		topElementsToSwitchBack = $("#indicator"),
		promoElements = $('.promo'),
		overview = $("#overview"),
		bullets = {
			"active" : $('<i/>').attr({
				"class" : "icon-circle",
				"aria-hidden" : "true"
			}),
			"inactive" : $('<i/>').attr({
				"class" : "icon-circle-empty",
				"aria-hidden" : "true"
			}) ,
			"overview" : $('<i/>').attr({
				"class" : "icon-layout",
				"aria-hidden" : "true"
			})
		},
		c = {
			'big' : 'big',
			'small' : 'small',
			'hide' : 'hide',
			'show' : 'show',
			'top' : 'top',
			'low' : 'low',
			'overview' : 'icon-layout',
			'active' : 'active'
		},
		c_ = function(selector) {
			return '.' + c[selector];
		};
	// private methods
	var init = function () {
		var winHeight = parseInt(win.height());
		tops.height(winHeight);
		if(body.attr('id') === "home") {
			verticalNavInit(winHeight);
			overview.css({
				'height' : 0,
				'overflow' : 'hidden',
				'opacity' : 0
			})
		}
		clickHandlers(winHeight);
	},
	verticalNavInit = function (winHeight) {
		var length = navElements.length,
			ul = verticalNav.find('ul'),
			width = 0,
			scrollingAmount = 100 / length;

		for(var i = 0; i < length; i++) {
			var bullet = bullets.inactive.clone();
			if(i == 0) {
				bullet = bullets.active.clone();
				promoElements.eq(i).addClass('active');
			}
			if (navElements.eq(i).attr('id') === 'overview') {
				bullet = bullets.overview.clone();
			}
			var li = $('<li/>').html(bullet);
			li.data({
				"scroll" : scrollingAmount * i,
				"color" : navElements.eq(i).attr("class")
			});
			ul.append(li);
			li.click(function () {
				var e = $(this);
				//loader.checkForImages(navElements.eq(e.index()));
				promoElements.removeClass('active');
				promoElements.eq(e.index()).addClass('active');
				loader.setActiveParent($('#main li.active').attr('id'));
				
				if(e.find('i').hasClass(c.overview)) {
					main.transition({
						'x' : $(this).data("scroll") * -1 + "%"
					}, 1500, 'snap', activateOverview);
				}
				else {
					main.transition({
						'x' : $(this).data("scroll") * -1 + "%"
					}, 1500, 'snap');
				}
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
			width += parseInt(li.outerWidth(true));
		}
		ul.css({
			"width" : width
		});
		verticalNav.css({
			"top" : winHeight - 150
		});
		scrollIndicator.css({
			"top" : winHeight - 90 - 100
		});
	},
	scrollDown = function (promoElement) {
		var e = promoElement,
			state = e.find(c_('top')).hasClass(c.small);
		if(state) {
			e.find(c_('top')).addClass(c.big);
			e.find(c_('low')).addClass(c.small);
		}
		else {
			e.find(c_('top')).addClass(c.small);
			e.find(c_('low')).addClass(c.big);
		}
	},
	activateOverview = function () {
		verticalNav.transition({
			'opacity' : 0
		}, 500, 'linear', function () {
			verticalNav.css('display', 'none');
		});
		overview.css({
			'height' : 'auto',
			'overflow' : 'visible'
		});
		overview.transition({
			'opacity' : 1
		}, 500, 'linear')
	},
	clickHandlers = function (winHeight) {
		win.scroll(function(event) {
			scrollDown(promoElements.filter('.active'));
		});
		scrollIndicator.click(function() {
			scrollDown(promoElements.filter('.active'));
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
	loader.init();
	loader.setActiveParent($('#main li.active').attr('id'));
	gaspi.init();
});