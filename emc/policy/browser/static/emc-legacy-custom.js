require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){ 
$('.collapse-control').on('click', function () {

var collapse_handler = $(this).attr('data-target');
var expanded = $(this).attr('aria-expanded');
var url = $(this).attr('href');

//controled component
var el = $(this).siblings('ul');
if (expanded == "false") {
	el.removeClass('collapse');
	el.addClass('collapse in');
	$(this).attr('aria-expanded', true);
// if current view is ajax_listings?
if ($('#searchResultDiv').length > 0){	
	$("#objid").attr("value", collapse_handler);
	searchEvent();
}
else {
	url = url + '/@@ajax_listings';
	window.location.href = url;
}	
} 
else {
	
	el.removeClass('in');
	//el.addClass('collapse');
	$(this).attr('aria-expanded', false);	
}
var willshow = $(this).find('.hidden');
var willhide = $(this).find('.shown');
 willshow.removeClass('hidden').addClass('shown');
 willhide.removeClass('shown').addClass('hidden');
 return false;
});
$('.nocollapse').on('click', function () {
var url = $(this).attr('href');	
// if current view is ajax_listings?
if ($('#searchResultDiv') !== null || $('#searchResultDiv') !==undefined){	
	$("#objid").attr("value", $(this).attr('data-id'));
	searchEvent();
}
else {
	url = url + '/@@ajax_listings';
	window.location.href = url;	
}	
 return false;	
});
// if current url is dropdown item
$('#navbar-collapse-kb-orm .dropdown-menu li a').on('click',function (){
	var url = $(this).attr('href');
	if (url.indexOf('jieshou') !== -1 || url.indexOf('fashe') !== -1){
		$(this).parent().parent().parent().addClass('active');
	}
	if (url.indexOf('bachang') !== -1 ){
		$(this).parent().parent().parent().addClass('active');
	}
	if (url.indexOf('ceshi') !== -1 ){
		$(this).parent().parent().parent().addClass('active');
	}		

});
// sage link to
$('a[href^="http://mw4024.wicp.net:8089/"]').attr('target','_blank').attr('class','outputlink');
});
});