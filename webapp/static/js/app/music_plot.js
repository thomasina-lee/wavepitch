
define([ 'jquery',  'd3' , 'd3tip'], function($, d3, d3tip) {

	

	var dimension = {
		width : 1400,
		height : 500,
		margin : 70
	};

	var svg_chart = d3.select("#music_chart_container")
					.append("svg")
					.attr("width", dimension.width + 2 * dimension.margin)
					.attr("height", dimension.height + 2 * dimension.margin)
					.append("svg:g").attr("class", "chart").attr("transform",
							"translate(" + dimension.margin + ", " + dimension.margin + ")");
	;



	svg_chart.append("svg:g").attr("id", "xaxis").attr("transform",
			"translate(" + 0 + ", " + (dimension.height) + ")");
	svg_chart.append("svg:g").attr("id", "yaxis");

	var position = 0;

	var colorScale = d3.scale.quantize().range(
			[ "#156b87", "#876315", "#543510", "#872815" ]).domain([ 0, 1 ]);


	
	

	var analyse_callback = function(data) {
		/**
		 * data is a JSON containing 
		 * note_names: array of note names
		 * note_numbers: internal node number, 
		 *              difference in note number denote difference in semi tone
		 *              and A(octave 4) = 57, and B(4) = 59 
		 *              (middle C is C(octave 4), C(4) = 48)
		 * time_values:  array of time in seconds
		 * active_notes:  array of {n (note_index), t (time_index), v (value of whether note is active)}
		 * 
		 */
    
    
    // process the data first
    data.active_notes = data.active_notes.map(function(d) {
      d.note_name = data.note_names[d.n];
      d.note_number = data.note_numbers[d.n];
      d.time_value = data.time_values[d.t];
      return d;
    });
    
		var max_time = (d3.max(data.active_notes, function(note_data){return note_data.time_value;}));
		var min_time = (d3.min(data.active_notes, function(note_data){return note_data.time_value;}));
		var max_note = (d3.max(data.active_notes, function(note_data){return note_data.note_number;}));
		var min_note = (d3.min(data.active_notes, function(note_data){return note_data.note_number;}));
		
		var time_delta =  (d3.max(data.time_values) - d3.min(data.time_values))/(data.time_values.length-1);
		
		
		var xscale = d3.scale.linear()
		            .domain([min_time - time_delta, max_time + time_delta])
		            .range([ 0, dimension.width ]);
		        

    
    
		var yscale = d3.scale.ordinal()
                .domain(d3.range(min_note, max_note + 1))
                .rangeBands([ dimension.height , 0]);
                
    var ydomain = data.note_numbers
                        .map(function(d, i){ return [d, data.note_names[i]];})
                        .filter(function(d){return d[0] >= min_note && d[0]<= max_note;})
                        .map(function(d){return d[1];});
    var yaxis_scale = d3.scale.ordinal()
                .domain(ydomain)
                .rangeBands([ dimension.height , 0]);
                
    var xaxis = d3.svg.axis().scale(xscale).orient("bottom");
    var yaxis = d3.svg.axis().scale(yaxis_scale).orient("left");
    
		var tip = d3.tip().attr('class', 'd3-tip')
		  .offset([-yscale.rangeBand()/2.0, 0])
		  .html(function(d) { 
		     return  "Time: " + d.time_value + ", Note: " + d.note_name; });
		   

    (d3.select('svg')).call(tip);
		
		// Display the axes.
		svg_chart.select("#xaxis").call(xaxis);
		svg_chart.select("#yaxis").call(yaxis);

		
		// Insert the data points.
		svg_chart.selectAll("rect")
			.data(data.active_notes).enter().append("rect")
			.attr("x", function(d) { return xscale(d.time_value - time_delta/2.0);})
			.attr("y", function(d) {return yscale(d.note_number );})
			.attr("width", function(d) {return Math.abs(xscale(time_delta) - xscale(0));})
			.attr("height", function(d) {return yscale.rangeBand();})
			.style("fill", function(d) {return colorScale(d.v);})
			//.on("mouseover", tip.show)
			//.on("mouseout", tip.hide)
			
      .on("mouseover", function() {
        
        var args = Array.prototype.slice.call(arguments);
        var d = args[0]; 
        
        d3.select("#music_note_detail input")
          .property("value", function() {
            if (d.v > 0) {
              return "Time: " + d.time_value + ", Note: " + d.note_name;
            } else {
              return " ";
            }
          });
         tip.show.apply(this, args);
           
      })

      .on("mouseout", function() {
        var args = Array.prototype.slice.call(arguments);
        
        d3.select("#music_note_detail input")
          .property("value", function() {
            return " ";
          });
        tip.hide.apply(this, args);
        
      })
     
		;

  $("#music_overlay").hide();
		
	};


  var error_callback = function (jqXHR, exception, _){
    $('#music_error_box').show();

  } ;
  
  var show_validation = function(ele){
     var val = ele.val();
     
      if (!(val.indexOf('http://', 0) === 0 || val.indexOf('https://', 0) ===0)){
        ele.parent().addClass('has-warning');
      } else {
        ele.parent().removeClass('has-warning');
      }
  
  };
  

	$(function() {
	  
	  
	  $("#music_overlay")
      .width($("#music_overlay").parent().width())
      .height($("#music_overlay").parent().height());
	  
    $('#music_error_box').hide();



    $('#music_error_box .close').on('click', function(e) {
        $(this).parent().hide();
    });


		$("#music_analyse button").click(function() {

			$("#music_overlay").show();
      $('#music_error_box').hide();
  
			$.ajax({
				url : "/analyse/",
				type : 'POST',
				data : {
					url : $("#music_analyse input").val()
				},
				dataType : "json",
				success : analyse_callback,
				error: error_callback
			});
			

		});


		
    $('#music_analyse input').keyup(function(e){
       
       show_validation($(this));
    });
    
 

	});



});