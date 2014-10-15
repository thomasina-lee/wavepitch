

requirejs.config({
	urlArgs:  "bust=" + (new Date()).getTime(),
	paths: {
		app: ".",
		d3: "../lib/d3.v3.min",
		underscore: "../lib/underscore-min",
		jquery: "../lib/jquery-2.1.1.min"
	},
	packages: [

	]
});

// Start the main app logic.
requirejs(['jquery', 'underscore', 'd3', 'app/music_plot'],
function   ( $,  _,  d3, musicPlot) {
	console.log("test");
    //jQuery, canvas and the app/sub module are all
    //loaded and can be used here now.
});