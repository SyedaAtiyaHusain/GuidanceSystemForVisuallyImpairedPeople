      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Confi. Level', {{dictionary["excited"]}}],
          
        ]);

        var options = {
          width: 500, height: 200,
          redFrom:0, redTo: 30,
          yellowFrom:30, yellowTo: 70,
          greenFrom: 70, greenTo: 100,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

        chart.draw(data, options);

        setInterval(function() {
          data.setValue(0,1,80);
          chart.draw(data, options);
        });
        
      }