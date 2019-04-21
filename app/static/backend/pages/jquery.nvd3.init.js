/**
* Theme: Minton Admin
* Author: Coderthemes
* Chart Nvd3 chart
*/


(function($) {
    'use strict';

    var graphTypeMap = {
      53: {
        selector: ".price-to-rent",
        title: "Price To Rent",
        xTitle: "Date",
        xFormat: d3.timeParse("%m %Y"),
        xTickFormat: d3.timeFormat("%m %Y"),
        yTitle: "Ratio",
        yFormat: d3.time.format("%m %Y"),
        yTickFormat: d3.format(',.2f')
      },
      56: {
        selector: ".median-rent",
        title: "Median List Price",
        xTitle: "Date",
        xFormat: d3.timeParse("%m %Y"),
        xTickFormat: d3.timeFormat("%m %Y"),
        yTitle: "Median Rent",
        yTickFormat: d3.format(".0f")
      }
    }

    function get(k){
      return graphTypeMap[k];
    }



    nv.addGraph(function() {
      $.get('/markets/get/region_data', {
        region_id: 102001,
      }).done(function(response) {
        var dataPointLength = response.dataPoints.length;
        Object.keys(graphTypeMap).forEach(function(key) {
          var values = [];
          var data = [];
          for (var i = 0; i < dataPointLength; i++) {
            if(response.dataPoints[i].type == key) {
              values.push({
                x: graphTypeMap[key]["xFormat"]("" + response.dataPoints[i].month + " " + response.dataPoints[i].year),
                y: response.dataPoints[i].value
              });
            }
          }
          data.push({
            values: values,      //values - represents the array of {x,y} data points
            key: response.region_name, //key  - the name of the series.
            color: '#' + (Math.random()*(1<<24)|0).toString(16).slice(2,8)  //color - optional: choose your own line color.
          });
          var height = 300;
          var lineChart = nv.models.lineChart();
          lineChart.useInteractiveGuideline(true);
          lineChart.xAxis.axisLabel(graphTypeMap[key]["xTitle"]).tickFormat(graphTypeMap[key]["xTickFormat"]);
          lineChart.yAxis.axisLabel(graphTypeMap[key]["yTitle"]).tickFormat(graphTypeMap[key]["yTickFormat"]);
          d3.select(graphTypeMap[key]["selector"] + ' svg')
            .attr('perserveAspectRatio', 'xMinYMid')
            .datum(data)
            .transition()
            .duration(0)
            .call(lineChart);
          nv.utils.windowResize(lineChart.update);
        });

        return;
      }).fail(function() {
        alert('An error occurred.');
      });
    });

})(jQuery);
