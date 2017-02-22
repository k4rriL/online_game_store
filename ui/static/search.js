$(function() {
    "use strict";

    $("#search").submit(function(event) {
      event.preventDefault();
      articleOffset = 0;
      window.location.replace("/")
    });
