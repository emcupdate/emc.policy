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
// sage link to
$('a[href^="http://mw4024.wicp.net:8089/"]').attr('target','_blank').attr('class','outputlink');
});
// ie check
var version = detectIE();
if (version && version <= 10) {
	alert("EMC推荐使用firefox/Chrome浏览器,以及IE11以上浏览器.您当前的IE版本为:" + version);
}
function detectIE() {
  var ua = window.navigator.userAgent;

  // Test values; Uncomment to check result …

  // IE 10
  // ua = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)';
  
  // IE 11
  // ua = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko';
  
  // Edge 12 (Spartan)
  // ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0';
  
  // Edge 13
  // ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586';

  var msie = ua.indexOf('MSIE ');
  if (msie > 0) {
    // IE 10 or older => return version number
    return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
  }

  var trident = ua.indexOf('Trident/');
  if (trident > 0) {
    // IE 11 => return version number
    var rv = ua.indexOf('rv:');
    return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
  }

  var edge = ua.indexOf('Edge/');
  if (edge > 0) {
    // Edge (IE 12+) => return version number
    return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
  }

  // other browser
  return false;
}
//end ie check
});