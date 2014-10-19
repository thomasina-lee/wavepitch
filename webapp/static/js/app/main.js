

requirejs.config({
	urlArgs:  "bust=" + (new Date()).getTime(),
	paths: {
		app: ".",
		d3: "../lib/d3.v3.min",
		underscore: "../lib/underscore-min",
		jquery: "../lib/jquery-2.1.1.min",
		bootstrap: "../lib/bootstrap-3.2.0.min"
	},
	shim: {
	  "bootstrap": {
	   deps: ["jquery"]
	  }
	}

});

// Start the main app logic.
requirejs(['jquery',  'bootstrap', 'd3', 'app/music_plot'],
function   ( $, bootstrap,  d3, musicPlot) {
	console.log("test");
    //jQuery, canvas and the app/sub module are all
    //loaded and can be used here now.
});