var indicator = (function ($) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		indicator = null,
		cookie = $.cookie,
		cookieName = 'linkId',
		posName = 'linkPos',
		parent = $('#navAndLogo .wrapper'),
		config = {
			'path': '/'
		},
		c = {
			'rdy': 'ready'
		},
		startValue = 'logo',
		defaultPos = {
			'left': 0,
			'width': 270
		};
	// private methods
	var init = function(indi) {
		cookie.json = true;
		indicator = indi;
		if(typeof getCookie() === "undefined" || window.location.pathname === '/gaspi/') {
			reset();
		}
		startPos(getPos());
		$(window).load(function(){
			newPos(getCookie());
		});
		clickHandlers();
	},
	startPos = function (pos) {
		indicator.css({ 
			'left': pos.left,
			'width': pos.width
		});
		
	},
	newPos = function (id) {
		var el = parent.find('#' + id);
		var offset = el.position();
		var pos = {
			'left': offset.left,
			'width': (id !== 'logo') ? el.width() -5 : el.width()
		}
		indicator.addClass(c.rdy);
		indicator.css(pos);
		indicator.one('transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd', function() {
			setPos(pos);
		});
	},
	setCookie = function (value) {
		cookie(cookieName, value, config);
	},
	setPos = function (pos) {
		cookie(posName, pos, config);
	},
	getPos = function () {
		return cookie(posName);	
	},
	getCookie = function () {
		return cookie(cookieName);
	},
	reset = function () {
		setCookie(startValue);
		setPos(defaultPos);
	},
	clickHandlers = function () {
		parent.find('a').click(function() {
			setCookie($(this).attr('id'));
			newPos(getCookie());
		});
	};
	// public methods
	module.init = function (indi) {
		init(indi);
	},
	module.setCookie = function (value) {
		setCookie(value);
	},
	module.resetCookie = function () {
		reset();
	};
	//return the module
	return module;
}(jQuery));

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
		m = false,
		next = 0,
		state = 'normal',
		activeParentId = false,
		c = {
			'home': 'home',
			'page': 'page',
			'notLoaded': 'notLoaded'
		}
	// private methods
	var check = function () {
		if (activeParentId) {
			var scrollOffset = doc.scrollTop();
			if(next === 0) { // setup check
				setupCheck();
			}
			// check
			if(next != false && scrollOffset >= next) { // we hit an image
				runImage(images[activeParentId][0]);
				// run again, just in case we scrolled alot
				setupCheck();
				check();
			}
		};
	},
	setupCheck = function () { // maybe make this smart?
		if(images[activeParentId].length > 0) {
			next = images[activeParentId][0].offset; // error when array empty
		}
		else {
			next = false;
		}
	},
	runImage = function (image) {
		var e = image.element;
		e.attr('src', e.data(state + '-src')).imagesLoaded(function (instance) {
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
	},
	setMediaState = function (Modernizr) {
		// test mediaqueries
		// set state
		// state = 'mobile';
	};
	// public methods
	module.checkForImages = function(parent) {
		parent.find('li').each(function(index, parent) {
			var p = $(parent);
			p.find(selector).each(function(cIndex, el){
				var e = $(el);
				addImage(e, p);
				if (state !== 'normal') {
					// unpack values
					var data = e.data(state);
					e.css( {
						'height' : data.height,
						'width' : data.width
					}).data(state + '-src', data.path).attr('src', '').addClass(c.notLoaded);
				}
				else {
					e.css('height', e.height()).data('normal-src', e.attr('src')).attr('src', '').addClass(c.notLoaded); // the height is the same for all images
				}
			});
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
		next = 0;
		activeParentId = parentID;
	},
	module.init = function (Modernizr) {
		setMediaState(Modernizr);
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
		nav = $('nav'),
		tops = $('.top'),
		verticalNav = $('#verticalNav'),
		scrollIndicator = $('#scrollIndicator'),
		topElementsToSwitchColor = $('nav li a, #logo'),
		topElementsToSwitchBack = $("#indicator"),
		promoElements = $('.promo'),
		overview = $("#overview"),
		scrollUpThreshold = 0,
		State = null,
		baseUrl = '/gaspi',
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
			'active' : 'active',
			'empty' : 'icon-circle-empty',
			'circle' : 'icon-circle',
			'scrollHeader': 'scrollHeader',
			'page' : 'page'
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
		if(body.hasClass(c.page)) {
			pageScroller();
		}
		clickHandlers(winHeight);
		// reset handler in nav
		$('#resetAndShowWorks').click(reset);
		// history.js
		(function(window,undefined){
		    // Bind to StateChange Event
		    History.Adapter.bind(window,'statechange', historyStateChange); // Note: We are using statechange instead of popstate
		})(window);
		State = History.getState();
		// promo item requested
		if (State.hash.indexOf('promo') != -1) {
			// split string
			var splitted = State.hash.split('/');
			var promoE = promoElements.filter('#' + splitted[splitted.length - 1]);
			var navE = verticalNav.find('li').eq(promoElements.index(promoE));
			
			setPromoElementActive(promoE);
			setVerticalNavElementActive(navE);

			mainMoveNormal(navE.data("scroll") * -1 + "%");
		};
		if(State.hash.indexOf('overview') != -1) {
			console.log("found overview");
			mainMoveNormal(verticalNav.find('li').last().data('scroll') * -1 + "%");
			activateOverview(0);
		};
	},
	historyStateChange = function () {
		State = History.getState();
		if (State.hash.indexOf('promo') != -1) {
			// split string
			var splitted = State.hash.split('/');
			var promoE = promoElements.filter('#' + splitted[splitted.length - 1]);
			var navE = verticalNav.find('li').eq(promoElements.index(promoE));
			
			setPromoElementActive(promoE);
			setVerticalNavElementActive(navE);

			mainMoveWithTransition(navE.data("scroll") * -1 + "%");
			if(verticalNav.css('display') === 'none') {
				deactiveOverview(1500);
			}
		};
		if(State.hash.indexOf('overview') != -1) {
			console.log("found overview");
			mainMoveWithTransition(verticalNav.find('li').last().data('scroll') * -1 + "%");
			activateOverview(0);
		};
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
				verticalNavClick(e);
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
	verticalNavClick = function (e) {
		//promoElements.removeClass('active');
		//promoElements.eq(e.index()).addClass('active');
		loader.setActiveParent($('#main li.active').attr('id'));
		//verticalNav.find('i.' + c.circle).toggleClass(c.circle).toggleClass(c.empty);
		//e.find('i').toggleClass(c.empty).toggleClass(c.circle);
		
		//mainMoveWithTransition(e.data("scroll") * -1 + "%");
		if(e.find('i').hasClass(c.overview)) {
			History.pushState(null, null, baseUrl + '/overview');
			activateOverview(1500);
		}
		else {
			History.pushState(null, null, baseUrl + '/promo/' + promoElements.eq(e.index()).attr('id'));
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
	},
	mainMoveWithTransition = function (percent) {
		main.transition({
			'x' : percent
		}, 1500, 'ease-in-out');
	},
	mainMoveNormal = function (percent) {
		main.transition({
			'x' : percent
		}, 0, 'linear');
	},
	setPromoElementActive = function (e) {
		promoElements.removeClass(c.active);
		e.addClass(c.active);
	},
	setVerticalNavElementActive = function (e) {
		verticalNav.find('i.' + c.circle).toggleClass(c.circle).toggleClass(c.empty);
		e.find('i').toggleClass(c.empty).toggleClass(c.circle);
	},
	scrollDown = function (promoElement) {
		var e = promoElement,
			state = e.find(c_('top')).hasClass(c.big);
		if(state && win.scrollTop() > 20) {
			disableScrolling();
			e.find(c_('top')).addClass(c.small).removeClass(c.big);
			e.find(c_('low')).addClass(c.big);
			var scroll = e.find(c_('scrollHeader')).height();
			win.scrollTop(scroll);
			win.off('scroll');
			win.on('scroll', function(event) {
				scrollUp(promoElements.filter('.active'));
			});
			hideVerticalNav(enableScrolling);
		}
	},
	doScrollUp = function (promoElement) {
		disableScrolling();
		win.off('scroll');
		var e = promoElement;
		e.find(c_('low')).addClass(c.small).removeClass(c.big);
		e.find(c_('top')).addClass(c.big).removeClass(c.small);
		verticalNav.css('display', 'block');
		showVerticalNav(function() {
			win.scroll('on', function(event) {
				scrollDown(promoElements.filter('.active'));
			});
			enableScrolling();
		});
	},
	scrollUp = function (promoElement) {
		var e = promoElement,
		state = e.find(c_('top')).hasClass(c.small);
		if(state) {
			var scrollValue = win.scrollTop();
			if(scrollValue === 0) {
				doScrollUp(e);
			}
		}
	},
	activateOverview = function (duration) {
		hideVerticalNav();
		overview.css({
			'height' : 'auto',
			'overflow' : 'visible'
		});
		overview.transition({
			'opacity' : 1
		}, duration + 500, 'linear');
	},
	deactiveOverview = function (duration) {
		showVerticalNav();
		overview.transition
		overview.transition({
			'opacity' : 0
		}, duration, 'linear', function() {
			overview.css({
				'height' : '0',
				'overflow' : 'hidden'
			});
		});
	},
	clickHandlers = function (winHeight) {
		win.on('scroll', function(event) {
			scrollDown(promoElements.filter('.active'));
		});
		scrollIndicator.click(function() {
			scrollDown(promoElements.filter('.active'));
		});
	},
	disableScrolling = function() {
		window.onmousewheel = document.onmousewheel = function(e) {
			e = e || window.event;
			if (e.preventDefault)
				e.preventDefault();
			e.returnValue = false;
		};
	},
	enableScrolling = function () {
		window.onmousewheel = document.onmousewheel = null;
	},
	hideMainMenu = function (callback) {
		toggleMainMenu(callback);
	},
	showMainMenu = function (callback) {
		toggleMainMenu(callback);
	},
	toggleMainMenu = function (callback) {
		nav.toggleClass(c.hide);
		if(callback) win.setTimeout(callback, 750);
	},
	hideVerticalNav = function (callback) {
		verticalNav.transition({
			'opacity' : 0
		}, 800, 'linear', function () {
			verticalNav.css('display', 'none');
			if(callback) callback();
		});
	},
	showVerticalNav = function (callback) {
		verticalNav.css('display', 'block');
		verticalNav.transition({
			'opacity' : 1
		}, 800, 'linear', function() {
			if(callback) callback();
		});
	},
	pageScroller = function () {
		body.find('a[href*="#"]').click(function(event) {
			event.preventDefault();
			var target = $("[name=" + $(this).attr("href").slice(1) + "]"),
				href = $(this).attr("href");
			$('html,body').animate({
          		scrollTop: target.offset().top
        	}, 1000, function () {
        		location.hash = href;
        		body.find(c_(c.active)).removeClass(c.active);
        		target.parent().addClass(c.active);
        		window.setTimeout(function() {
        			target.parent().removeClass(c.active);
        		}, 2000);
        	});
		});
	},
	reset = function () {
		console.log("stuff");
	};
	// public methods
	module.init = function () {
		init();
	};
	//return the module
	return module;
}(jQuery));

jQuery(document).ready(function($) {
	loader.init(Modernizr);
	loader.setActiveParent($('#main li.active').attr('id'));
	gaspi.init();
	indicator.init($('#indicator'));
});