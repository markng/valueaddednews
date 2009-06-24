$(document).ready(function() {
	var slides = $('.code-slide');
	var speed = 300;
	slides.hide() // hide them
	slides.slice(0,1).show() // show first

	// add next/previous controls
	slides
		.children('div.code-title')
		.append("<div class='code-selector'><a class='prev'>&lt;</a> <a class='next'>&gt;</a></div>");
	// remove start and end controls
	slides.children('div.code-title div.code-selector a:first').hide();
	slides.children('div.code-title div.code-selector a:last').hide();
	
	slides.children('div.code-title div.code-selector a:eq(1)');
	
	slides
		.children('div.code-title')
		.children('div.code-selector')
		.children('a')
		.click(function() {
			var thislink = $(this);
			console.log(thislink);
			if (thislink.hasClass('next')) {
				var ggparent = thislink.parent().parent().parent();
				var gguncle = thislink.parent().parent().parent().next();
				ggparent.hide('slide',{},speed, function () { gguncle.show('slide',{},speed) });
			};
			if (thislink.hasClass('prev')) {
				var ggparent = thislink.parent().parent().parent();
				var gguncle = thislink.parent().parent().parent().prev();
				ggparent.hide('slide',{},speed, function () { gguncle.show('slide',{},speed) });
			};
		});
});
