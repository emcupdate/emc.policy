require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){ 
  // we're creating a singleton here so we can potentially
  // delay the initialization of the translate catalog
  // until after the dom is available
$('.collapse-control').on('click', function () {
var willshow = $(this).find('.hidden');
var willhide = $(this).find('.shown');
 willshow.removeClass('hidden').addClass('shown');
 willhide.removeClass('shown').addClass('hidden');
});
$('a[href^="http://mw4024.wicp.net:8089/"]').attr('target','_blank').attr('class','outputlink');
});
});