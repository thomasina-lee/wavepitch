

define(['jquery', 'underscore', 'd3'], function($, _, d3) {

	
	console.log("hello x");
		
	var dimension = {
	  width : 1400,
	  height: 1000,
	  margin : 100
	}
		
	var svg_chart = d3.select("#chart_container")
	            .append("svg")
	            .attr("width", dimension.width + 2 * dimension.margin)  
              .attr("height", dimension.height + 2 * dimension.margin)
              
	            .append("svg:g")
	            .attr("class", "chart")
	            .attr("transform", "translate(" + dimension.margin + ", "  + dimension.margin  + ")");
	            ;
  
  //svg_chart.append("circle").attr("cx", 0).attr("cy", 0).attr("r", 200);
  
	svg_chart.append("svg:g")
	 .attr("id", "xaxis")
	 .attr("transform", "translate(" + 0 + ", " + (dimension.height ) + ")");
	svg_chart.append("svg:g").attr("id", "yaxis")

	var position = 0; 
  
  var colorScale = d3.scale.quantize()
              .range(["#156b87", "#876315", "#543510", "#872815"])
              .domain([0, 1]);

	var xscale = d3.scale.ordinal().rangeBands([0,dimension.width]);
	var yscale = d3.scale.ordinal().rangeBands([dimension.height,0]);
	var xaxis = d3.svg.axis().scale(xscale).orient("top");
	var yaxis = d3.svg.axis().scale(yscale).orient("left");
  
  
  
	var analyse_callback = function (data) {
	  /**
	   * data is a JSON containing 
	   * note_names: array of note names
	   * time_values:  array of time in seconds
	   * active_notes:  array of (note_nmr, time_nmr, note_active)
	   * 
	   */ 
	 
    // Rescale the axes.
    console.log("start callback");
    
    console.log(data);
    xscale.domain(data.time_values);
    yscale.domain(data.note_names);


    // Display the axes.
    data.active_notes = data.active_notes
      .map(function(d){
        d.note_name = data.note_names[d.n]; 
        d.time_value = data.time_values[d.t]; 
        return d;
      });
   
    console.log(data);
    // Display the axes.
    svg_chart.select("#xaxis").call(xaxis);
    svg_chart.select("#yaxis").call(yaxis);

    console.log("set scale");

    // Insert the data points.
    svg_chart.selectAll("rect").data(data.active_notes).enter()
        .append("rect")
            .attr("x", function (d) { return xscale(d.time_value); })
            .attr("y", function (d) { return yscale(d.note_name); })
            .attr("width", function (d) { return xscale.rangeBand(); })
            .attr("height", function (d) { return yscale.rangeBand(); })
            .style("fill", function (d) { return colorScale(d.v); })
            .attr("title", function(d) {return "Time: " + d.time_value + ", Note: "+ d.note_name; })
            .on("mouseover", function(d) {
       
                d3.select("#note_detail input")
                  .property("value", function (){ 
                     if (d.v > 0){
                           return "Time: " + d.time_value + ", Note: "+ d.note_name;
                     }
                     else{
                           return " ";
                      }
                  });
              })
            .on("mouseout", function(d){
              d3.select("#note_detail input")
                  .property("value", function (){ 
                     return " ";
                  });
              
            })
                           
         ;
  };
  
  
  $(function(){
	   $("#file_analyse button").click(function(){
    		console.log("hello1");
    		console.log($("#file_analyse select").val());

  		$.ajax({
  		  url: "/analyse/",
  		  type: 'POST',
  		  data: { filename: $("#file_analyse select").val() },
  		  dataType: "json",
  		  success: analyse_callback
  		});
  		//svg_chart.append("circle")
  		//	.attr("cx", 50)
  		//	.attr("cy", 5)
  		//	.attr("r", 10);
  	});
  	
  	$("#chart_container rect").tooltip({
        'container': 'body',
        'placement': 'right'
    });
  
  });
  

	
	//d3.select("#file_submit").on("click", 
	//);
	
			
	
	
	
});