/**
* Theme: Minton Admin
* Author: Coderthemes
* Chart Nvd3 chart
*/


(function($) {
    'use strict';

    nv.addGraph(function() {
      var parseDate = d3.timeParse("%m %Y");
      var format = d3.time.format("%m %Y");
      var myData = [{
          {% record in data_records %}
            values: [
                {x: parseDate("01 2011"), y: "1.23"},
                {x: parseDate("02 2011"), y: "1.24"}
              ],      //values - represents the array of {x,y} data points
            key: '{{ record.region_name }}', //key  - the name of the series.
            color: '#ff7f0e'  //color - optional: choose your own line color.
          }
          {% endfor %}
        ];
        var lineChart = nv.models.lineChart();
        var height = 300;
        lineChart.useInteractiveGuideline(true);
        lineChart.xAxis.axisLabel('Month Year').tickFormat(d3.timeFormat("%m %Y"));
        lineChart.yAxis.axisLabel('Price-to-Rent Ratio').tickFormat(d3.format(',.2f'));
        d3.select('.line-chart svg').attr('perserveAspectRatio', 'xMinYMid').datum(myData).transition().duration(500).call(lineChart);
        nv.utils.windowResize(lineChart.update);
        return lineChart;
    });

})(jQuery);
