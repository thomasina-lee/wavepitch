

requirejs.config({
	urlArgs:  "bust=" + (new Date()).getTime(),
	paths: {
		app: ".",
		d3: "../lib/d3.v3.min",
		underscore: "../lib/underscore-min",
		jquery: "../lib/jquery-2.1.1.min",
		bootstrap: "../lib/bootstrap-3.2.0.min",
		d3tip: "../lib/d3-tip.v0.6.3"
	},
	shim: {
	  "bootstrap": {
	     deps: ["jquery"]
	  },
	  "d3tip":{
	     deps: ["d3"]
	  }
	}

});

// Start the main app logic.
requirejs(['jquery',  'bootstrap', 'd3', 'd3tip','app/music_plot'],
function   ( $, bootstrap,  d3, d3tip, musicPlot) {
	console.log("test");
    //jQuery, canvas and the app/sub module are all
    //loaded and can be used here now.
});