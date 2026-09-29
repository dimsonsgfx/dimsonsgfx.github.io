function showOverlay(){
	$('.overlay-box').fadeIn(200);
};
function hideOverlay(){
	$('.overlay-box').fadeOut(200);
};
$(document).ready(function(){
	
	$('body').on('click','.js-login',function(){
		showOverlay();
		$('.login-box').fadeIn(200);
		return false;
	});
	$('body').on('click','.js-search',function(){
		showOverlay();
		$('.search-wrap').fadeIn(200).find('.search-box input').focus();
	});
	$('body').on('click','.overlay-box, .login-close, .search-close, .btn-close',function(){
		$('.login-box, .search-wrap').fadeOut(200);
		$('#side-panel, .btn-close').removeClass('active');
		$('body').removeClass('opened-menu');
		hideOverlay();
	});
	
	$('body').append('<div class="overlay-box hidden"></div><div class="side-panel" id="side-panel"></div><div class="btn-close"><span class="far fa-times"></span></div><div id="gotop"><span class="fas fa-chevron-up"></span></div>');
	$('.to-mob').each(function() {
		$(this).clone().appendTo('#side-panel');
	});		
	$(".btn-menu").click(function(){
		showOverlay();
		$('#side-panel, .btn-close').addClass('active');
		$('body').addClass('opened-menu');
	});
	
	$('.js-author').each(function(){
        var a = $(this), b = a.closest('.js-comm'), c = a.text().substr(0,1), 
            f = b.find('.js-avatar'), e = f.children('img').attr('src'),
			d = ["#c57c3b","#753bc5","#79c53b","#eb3b5a","#45aaf2","#2bcbba","#778ca3"], rand = Math.floor(Math.random() * d.length);
		if (e == '/templates/'+dle_skin+'/dleimages/noavatar.png') {
            f.html('<div class="comm-letter" style="background-color:'+d[rand]+'">'+c+'</div>');
		};
    });	
	
	$('body').on('click','.faddcomms',function(){
		$(".fcomms").slideToggle(200);
	});
	$('body').on('click','.reply',function(){
		$("#add-comms").slideDown(200);
	});
	$('body').on('click','.ac-textarea textarea, .fr-wrapper',function(){
		$('.add-comms').addClass('active').find('.ac-protect').slideDown(400);
	});

    $('#dle-content > #dle-ajax-comments').appendTo($('#full-comms')); 
	
	var $gotop=$('#gotop'); 
	$(window).scroll (function () {
		if ($(this).scrollTop () > 300) {$gotop.fadeIn(200);
		} else {$gotop.fadeOut(200);}
	});	
	$gotop.click(function(){
		$('html, body').animate({ scrollTop : 0 }, 'slow');
	});
	
});


/* end */