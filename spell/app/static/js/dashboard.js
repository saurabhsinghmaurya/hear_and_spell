function createPie(div, title, data){
    Highcharts.setOptions({
             colors: ['#E0E0E0', '#FF9933', '#d9534f', '#990000']
            });
    chartdata = JSON.parse(JSON.stringify(data))

    $('#'+div).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        credits: {
             enabled: false
        },
        title: {
            text: title
        },
        series: chartdata.series
    });
}

function createPieLegend(div, title, data){
Highcharts.setOptions({
             colors: ['#E0E0E0', '#FF9933', '#d9534f', '#990000']
            });
    chartdata = JSON.parse(JSON.stringify(data))

    $('#'+div).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false,
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                },
                showInLegend: true
            }
        },
        credits: {
             enabled: false
        },
        title: {
            text: title
        },
        series: chartdata.series
    });
}

function createLine(div, title, data){
    chartdata = JSON.parse(JSON.stringify(data))
    $('#'+div).highcharts({
        title: {
            text: title,
            x: -20 //center
        },
        xAxis: {
            categories: chartdata.xaxis
        },
        yAxis: {
            title: {
                text: chartdata.yaxis
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: chartdata.unit
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: chartdata.series
    });
}

function createBar(div, title, subtitle, ytitle, data) {
    Highcharts.setOptions({
                     colors: ['#87CEFA', '#0000CD']
                    });
    chartdata = JSON.parse(JSON.stringify(data))
    console.log(chartdata)
    // Create the chart
    $('#'+div).highcharts({
        chart: {
            type: 'column',
            text: 'Component Names'
        },
        title: {
            text: title
        },
        subtitle: {
            text: 'Total Sensei Bug Count:' + subtitle
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: ytitle
            }

        },
        legend: {
            enabled: false,
        },
        credits: {
             enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
        },
        series: chartdata.series
    });
}

function createTable(div, data){
    // var processed_json = new Array();
    // $.map(json, function(obj, i) {
    //     processed_json.push([obj.key, parseInt(obj.value)]);
    // });

    chartdata = JSON.parse(JSON.stringify(data));

    console.log(chartdata.field_names)
    //console.log(chartdata.field_data)
    var colData = chartdata.field_names

    // var rowData = processed_json ;//[["111","Ryan Connolly"], ["10","Julie Connolly"], ["5","Chloe Connolly"]];
    var rowData = chartdata.field_data ;
    var data = {"Cols":colData, "Rows":rowData};

    var table = $('<table/>').attr("id", "userquerytable"+div).addClass("display").attr("cellspacing", "0").attr("width", "100%");

    var tr = $('<tr/>');
    table.append('<thead>').children('thead').append(tr);

    for (var i=0; i< data.Cols.length; i++) {
        tr.append('<td>'+data.Cols[i]+'</td>');
    }

    for(var r=0; r < data.Rows.length; r++){
        var tr = $('<tr/>');
        table.append(tr);
        //loop through cols for each row...
        for(var c=0; c < data.Cols.length; c++){
            tr.append('<td>'+data.Rows[r][c]+'</td>');
        }
    }

    $('#'+div).append(table);


    $('#userquerytable'+div).DataTable({
        responsive: true
    });
}

function createColumnDrillDown(div, title, subtitle, data) {
    // Create the chart
    //
    Highcharts.setOptions({
                     colors: ['#87CEFA', '#0000CD']
                    });

    chartdata = JSON.parse(JSON.stringify(data))
    $('#'+div).highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: title
        },
        subtitle: {
            text: subtitle
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'Bug Count'
            }

        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
        },

        series: chartdata.series,
        drilldown: chartdata.drilldown
    });
}

function createBasicLine(div, title, subtitle, ytitle, data) {

    chartdata = JSON.parse(JSON.stringify(data))

    $('#'+div).highcharts({
        title: {
            text: title,
            x: -20 //center
        },
        subtitle: {
            text: subtitle,
            x: -20
        },
        xAxis: {
            categories:  chartdata.categories
        },
        yAxis: {
            title: {
                text: ytitle
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: ''
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: chartdata.series
    });
}

