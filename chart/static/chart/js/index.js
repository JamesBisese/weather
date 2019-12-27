
var orgHighchartsRangeSelectorPrototypeRender = Highcharts.RangeSelector.prototype.render;

Highcharts.RangeSelector.prototype.render = function (min, max)
{
	orgHighchartsRangeSelectorPrototypeRender.apply(this, [min, max]);

	var leftPosition = this.chart.plotLeft,
		topPosition = this.chart.plotTop - 100,
		space = 2;

	this.zoomText.attr({
		x: leftPosition,
		y: topPosition + 15
	});

	leftPosition += this.zoomText.getBBox().width;
	for (var i = 0; i < this.buttons.length; i++)
	{
		this.buttons[i].attr({
			x: leftPosition,
			y: topPosition
		});
		leftPosition += this.buttons[i].width + space;
	}
};

function change_station() {
	var stationDom = document.getElementById("station");
	var stationBDom = document.getElementById("stationB");
	var site_codeA = stationDom.value;
	var site_codeB = stationBDom.value;

	var chart = document.getElementById('HighChartContainer');
	var hchart = Highcharts.charts[chart.getAttribute('data-highcharts-chart')];
	hchart.setTitle({text: 'Air Temperature and Air Pressure at ' + site_codeA});
	hchart.setTitle(null, {text: 'Air Temperature and Air Pressure at ' + site_codeB});

	hchart.setTitle({text: 'Air Temperature at ' + site_codeA});
	hchart.setTitle(null, {text: 'Air Temperature at ' + site_codeB});


	requestData(hchart, site_codeA, site_codeB);
}

function requestData(hchart, site_codeA, site_codeB) {
    $.ajax({
        url: '/data/weather/' + site_codeA + '/',
        type: "GET",
        dataType: "json",
        data : {username : "demo"},
        success: function(data) {
        	addData(hchart, site_codeA, 0, data);
        },
        cache: false
    });
    $.ajax({
        url: '/data/weather/' + site_codeB + '/',
        type: "GET",
        dataType: "json",
        data : {username : "demo"},
        success: function(data) {
            addData(hchart, site_codeB, 2, data);
        },
        cache: false
    });
}

function addData(hchart, site_code, series_id, data){
	var airtemp_data = [];
	var pressure_data = [];
	data.forEach(function(obs){
		airtemp_data.push([obs.timestamp * 10, obs.airtemp]);
		// pressure_data.push([obs.timestamp * 10, obs.airpressure]);
	});
	hchart.series[series_id].name = site_code + " Air Temperature";
	hchart.series[series_id].setData(airtemp_data);
	// hchart.series[series_id + 1].name = site_code + " Air Pressure";
	// hchart.series[series_id + 1].setData(pressure_data);
}


function show_table()
{
	//alert('soon I will show table');
    var chart = Highcharts.charts[0];
    var chartDiv = $(chart.renderTo);

    if (chartDiv.is(":visible")) {
        chartDiv.hide();
        if (!chart.dataTableDiv) {

            chart.update({
                exporting: {
                    showTable: true
                }
            });
            let height = $(chart.dataTableDiv).height();
            $(".make_radius_border").css({'bottom': (height * -1).toString() + 'px'});
        } else {
            $(chart.dataTableDiv).show();
            let height = $(chart.dataTableDiv).height();
            $(".make_radius_border").css({'bottom': (height * -1).toString() + 'px'});
        }
    } else {
        chartDiv.show();
        $(chart.dataTableDiv).hide();
        $(".make_radius_border").css({'bottom': '22px'});
    }
}

$(function ()
{
	$('#HighChartContainer').highcharts('StockChart',
	{
		chart:
		{
			type: 'spline',
			zoomType: 'x',
			borderWidth: 2,
			borderRadius: 20,
			borderColor: '#005596',
			renderTo: 'container'
		},
		navigator:
		{
			height: 60,
			margin: 5
		},
		legend:
		{
			layout: 'vertical',
			floating: 'true',
			verticalAlign: 'top',
			align: 'right',
			y: -14
		},
		title:
		{
			text:  "<?php echo 'Air Temperature and Air Pressure at ' . $site_code . ' - ' . $site_name; ?>",
			style: {
				fontFamily: "'Open Sans', Helvetica, Arial"
			}
		},
		subtitle:
		{
			text:  "<?php echo 'Shown against Air Temperature and Air Pressure at ' . $site_codeB . ' - ' . $site_nameB; ?>",
			style: {
				fontFamily:  "'Open Sans', Helvetica, Arial"
			}
		},
		xAxis:
		{
			type: 'datetime',
			title: {
				text: 'Date'
			},
			gridLineWidth: 1,
			minorGridLineWidth: 0,
			range: 3 * 24 * 3600 * 1000,
			events:
			{
				afterSetExtremes: function(e)
				{
					var maxDistance = 3 * 30 * 24 * 3600 * 1000; //3 months time
					var xaxis = this;
					if ((e.max - e.min) > maxDistance)
					{
						var min = e.max - maxDistance;
						var max = e.max;
						window.setTimeout(function() {
							xaxis.setExtremes(min, max);
						}, 1);
					}
				}
			}
		},
		rangeSelector:
		{
			buttonTheme:
			{ // styles for the buttons
				fill: 'none',
				stroke: 'none',
				'stroke-width': 0,
				r: 8,
				style:
				{
					color: '#039',
					fontWeight: 'bold'
				},
				states:
				{
					hover: { },
					select:
					{
						fill: '#039',
						style: {
							color: 'white'
						}
					}
				}
			},
			inputBoxBorderColor: 'gray',
			inputBoxWidth: 100,
			inputBoxHeight: 18,
			inputStyle: {
				color: '#039',
				fontWeight: 'bold',
				fontFamily: "'Open Sans', Helvetica, Arial"

			},
			labelStyle: {
				color: 'silver',
				fontWeight: 'bold',
				fontFamily: "'Open Sans', Helvetica, Arial"
			},
			selected: 1,
			buttons:
			[
				{
					type: 'day',
					count: 1,
					text: '1d'
				},
				{
					type: 'day',
					count: 3,
					text: '3d'
				},
				{
					type: 'week',
					count: 1,
					text: '1w'
				},
				{
					type: 'week',
					count: 2,
					text: '2w'
				},
				{
					type: 'week',
					count: 3,
					text: '3w'
				},
				{
					type: 'all',
					text: '3M'
				}
			]
		},
		yAxis:
		[
			{ // primary axis
				opposite: false,
				title:
				{
					text: 'Air Temperature (\xB0F)'
				},
				labels:
				{
					format: '{value} \xB0F'
				}
			},
			{ // secondary axis
				opposite: true,
				gridLineWidth: 0,
				title:
				{
					// text: 'Air Pressure (inches)',
					style: {
						color: Highcharts.getOptions().colors[0]
					}
				},
				labels:
				{
					format: '{value} in.',
					style: {
						color: Highcharts.getOptions().colors[0]
					}
				}
			}
		],
		plotOptions:
		{
			series:{
				dataGrouping: { enabled: false },
				connectNulls: false
				}
		},
		series:
		[
			{
				name: 'site_codeA Air Temperature',
				// data: "<?php echo json_encode($timeseriesA); ?>",
				color: '#FF0000'
			},
			{
				name: 'site_codeA Air Pressure',
				// data: "<?php echo json_encode($timeseriesA_pressure); ?>",
				color: '#FFCCFF',
				yAxis: 1,
				marker: {
					enabled: false
				}
			},
			{
				name: 'site_codeB Air Temperature',
				// data: "<?php echo json_encode($timeseriesB);  ?>",
				yAxis: 0,
				color: '#0000FF'
			},
			{
				name: 'site_codeB Air Pressure',
				// data: "<?php echo json_encode($timeseriesB_pressure); ?>",
				yAxis: 1,
				marker: {
					enabled: false
				},
				color: '#66CCFF'
			}
		]
	});
});

// onready function - load data for automatically selected set
$(function () {
	change_station();
});