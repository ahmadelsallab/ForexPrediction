var chartsObjects = {};

//function for bar width , the function calculates every series and check's maxPointWidth
jQuery(function () {
    (function(H) {
        var each = H.each;
        H.wrap(H.seriesTypes.column.prototype, 'drawPoints', function(proceed) {
            var series = this;
            var appendWidth = (series.options.appendWidth) != undefined ? series.options.appendWidth : 0;
            if (series.data.length > 0) {
                var width = series.barW > series.options.maxPointWidth ? series.options.maxPointWidth : series.barW + appendWidth;
                each(this.data, function(point) {
                    point.shapeArgs.x += (point.shapeArgs.width - width) / 2;
                    point.shapeArgs.width = width;
                });
            }
            proceed.call(this);
        })


    })(Highcharts);
});


//abstract chart class
function ChartParent(divId) {


    this.series;
    this.categoriesLabels;
    this.categories;
    this.onclickResponse = [];
    this.parseAsTime = false;
    this.hasDataText = false;
    this.legendNoLimit = false;
    this.divId = divId;
    this.sNumberSuffix = '';
    this.numberSuffix = '';
    this.prefix = '';
    this.sprefix = '';
    this.showSeriesName = true;
    this.sharedTooltip = false;
    this.maxDivXLines = 5;
    this.maxDivYLines = 5;
    this.gridLineWidth = 1;
    this.titleSize = '11px';

    this.options = {
        colors: ["rgba(180, 134, 180, 1)","rgba(226, 134, 134, 1)","rgba(90, 180, 180, 1)","rgba(255, 183, 137, 0.9)","rgba(181, 211, 93, 0.9)","rgba(246, 210, 99, 0.9)","rgba(204, 230, 250, 0.9)","rgba(203, 198, 90, 0.9)","rgba(192, 175, 210, 0.9)","rgba(146, 174, 114, 0.9)","rgba(192, 98, 101, 0.9)","rgba(90, 180, 226, 0.9)"],

        lang: {
            //customize the no data message
            noData: ''
        },
        noData: {
            position :{  x: 0, y: 0,  verticalAlign: "middle"}
        },
        chart:  {
            renderTo: this.divId
        },

        title: {
            text: null,
            style: {
                fontSize: this.titleSize,
                fontFamily: 'Arial',
                fontWeight: 'bold'

            }
        },
        labels: {
            style: {
                fontSize: '11px',
                fontFamily: 'Arial'
            }
        }
        ,
        credits: {
            enabled: false
        },
        series: [],
        legend: {
            useHTML: true,
            x: 30,
            margin: 2,
            itemStyle: {
                fontSize:'11px',
                color: '#666666',
                fontWeight:'normal'
            }
        }
    };

    this.setEmptyMessage = function(noData) {
        if (jQuery.browser.msie  && jQuery.browser.version <=8) {
            this.options.lang.noData = noData;
        }
    };

    this.isEmpty = function() {
        return this.options.series.length == 0;
    };
    this.getOptions = function() {
        return this.options;
    };

    this.render = function(value) {
        if (Math.abs(value) >= 1000 && Math.abs(value) < 1000000) {
            return this.toFixed((value / 1000), 1000) + 'K';
        } else if (Math.abs(value) >= 1000000) {
            return this.toFixed((value / 1000000), 1000000) + 'M';
        }
        return  this.toFixed(value, 100);
    };

    //fixed and round big numbers
    this.toFixed = function(num, fixed) {
        return Math.round(num * fixed) / (fixed);
    };

    //check for which yaxis show suffix
    this.checkSuffix = function(series) {
        if (series.type == "column") {
            return this.sNumberSuffix;
        } else {
            return this.numberSuffix;
        }
    };


    //check for which yaxis show suffix
    this.checkPrefix = function(series) {
        if (series.type == "column") {
            return this.sprefix;
        } else {
            return this.prefix;
        }
    };


    //chnage duration to num+str
    this.duration = function(millis) {
        var m = millis;
        var week = Math.floor(m / WEEK);
        m -= week * WEEK;
        var days = Math.floor(m / DAY);
        m -= days * DAY;
        var hours = Math.floor(m / HOUR);
        m -= hours * HOUR;
        var minutes = Math.floor(millis / MINUTE);
        m -= minutes * MINUTE;
        var seconds = Math.floor(m / SECOND);

        if (week > 0) {
            return this.toFixed(millis / WEEK, 100) + "wk";
        } else if (days > 0) {
            return this.toFixed(millis / DAY, 100) + "day";
        } else if (hours > 0) {
            return this.toFixed(millis / HOUR, 100) + "hr";
        } else if (minutes > 0) {
            return this.toFixed(millis / MINUTE, 100) + "min";
        } else {
            return this.toFixed(millis / SECOND, 100) + "sec";
        }
    };

    this.initData = function(json, type) {
        if (hasText(json.categories)) {
            if (type == 0) {
                this.options.xAxis.categories = json.categories;
            } else {
                this.options.xAxis.tickPositions = json.categories;
            }
            this.categories = json.categories;

        }
        if (hasText(json.series)) {
            this.options.series = json.series;
            this.series = json.series;
            if (this.series.length > 0) {
                if (this.series[0].dataText != undefined) {
                    this.hasDataText = true;
                }
            }

        }
        if (hasText(json.title)) {
            this.options.title.text = json.title;
        }

        if (json.xAxisTitle) {
            this.options.xAxis.title.text = json.xAxisTitle;
        }
        if (json.categoriesFontSize && this.options.xAxis) {
            this.options.xAxis.labels.style.fontSize = json.categoriesFontSize;
        }
        if (json.categoriesFont && this.options.xAxis) {
            this.options.xAxis.labels.style.fontFamily = json.categoriesFont;
        }
        if (hasText(json.categoryRotation)) {
            this.options.xAxis.labels.rotation = json.categoryRotation;
        }


        if (json.categoriesLabels) {
            this.categoriesLabels = json.categoriesLabels;
        }
        if (json.onclickResposne) {
            this.onclickResponse = json.onclickResposne;
            this.options.plotOptions.series.cursor = 'pointer'
        }

        if (json.colorByPoint) {
            this.options.plotOptions.series.colorByPoint = true;
        }

        if (hasText(json.sNumberSuffix)) {
            this.sNumberSuffix = json.sNumberSuffix;
        }

        if (hasText(json.numberSuffix)) {
            this.numberSuffix = json.numberSuffix;
        }

        if (hasText(json.prefix)) {
            this.prefix = json.prefix;
        }

        if (hasText(json.sprefix)) {
            this.sprefix = json.sprefix;
        }

        if (hasText(json.showSeriesName)) {
            this.showSeriesName = json.showSeriesName;
        }

        if (hasText(json.parseAsTime)) {
            this.parseAsTime = json.parseAsTime;
        }

        if (hasText(json.showStackLabels)) {
            this.options.yAxis.stackLabels.enabled = json.showStackLabels;
        }

        if (!(hasText(json.legendNoLimit) || json.legendNoLimit)) {
            this.options.legend.itemWidth = 180;
            this.options.legend.labelFormatter = function() {
                if (this.name.length > 25) {
                    return this.name.slice(0, 25) + '...'
                }
                else {
                    return this.name
                }
            };
        }

        if (hasText(json.appendWidth) && json.appendWidth) {
            this.options.plotOptions.series.appendWidth = json.appendWidth
        }

        if (hasText(json.colors) && json.colors) {
            this.options.colors = json.colors
        }
        if (hasText(json.pointRadius) && json.pointRadius) {
            this.options.plotOptions.scatter.marker.radius = json.pointRadius
        }
        if (hasText(json.sharedTooltip) && json.sharedTooltip) {
            this.options.tooltip.shared = json.sharedTooltip;
            this.sharedTooltip = json.sharedTooltip;
        }

        if (hasText(json.maxPointWidth)) {
            this.options.plotOptions.series.maxPointWidth = json.maxPointWidth;
            this.sharedTooltip = json.sharedTooltip;
        }
        if (hasText(json.maxDivXLines)) {
            this.maxDivXLines = json.maxDivXLines;
        }
        if (hasText(json.maxDivYLines)) {
            this.maxDivYLines = json.maxDivYLines;
        }

        if (hasText(json.gridLineWidth)) {
            this.gridLineWidth = json.gridLineWidth;
        }

        if (hasText(json.titleSize)) {
            this.titleSize = json.titleSize;
            this.options.title.style.fontSize = this.titleSize;
        }
    };
}

// all classes inherit chart parent abstract class
LineColumnChart.prototype = new ChartParent();
LineColumnChart.prototype.parent = ChartParent.prototype;
StackColumn.prototype = new ChartParent();
StackColumn.prototype.parent = ChartParent.prototype;
ColumnChart.prototype = new ChartParent();
ColumnChart.prototype.parent = ChartParent.prototype;
ScatterChart.prototype = new ChartParent();
ScatterChart.prototype.parent = ChartParent.prototype;
PieChart.prototype = new ChartParent();
PieChart.prototype.parent = ChartParent.prototype;
SimpleLineChart.prototype = new ChartParent();
SimpleLineChart.prototype.parent = ChartParent.prototype;

function LineColumnChart(divId) {

    this.parent.constructor.call(this, divId);
    var parent = this;

    this.options.chart = {
        animation:false,
        renderTo: this.divId,
        zoomType: 'x',
        plotBorderColor:'#ECEBEB',
        plotBorderWidth:1,
        style: {
            fontSize:'11px',
            fontWeight:'normal'
        },
        events: {
            selection: function (event) {
                try {
                    if (event.xAxis) {
                        var extremesObject = event.xAxis[0],
                            min = extremesObject.min,
                            max = extremesObject.max;
                        calculatePointRadius(this, max - min);
                    } else {
                        calculatePointRadius(this, parent.categories.length);
                    }
                } catch(e) {
                }
            }
        }
    };

    this.options.xAxis = {
        labels: {
            style: {
                fontSize: '11px',
                fontFamily: 'Arial'
            }
        },
        categories: [] ,
        gridLineColor: '#ECEBEB',
        gridLineWidth:parent.gridLineWidth       ,
        startOnTick:true,
//            showFirstLabel: true,
        tickColor:'#ffffff',
        //calculate the labels ticks
        tickPositioner: function (min, max) {
            var t = [];
            var minInterval = max - min;
            var tick = Math.floor(minInterval / parent.maxDivXLines);
            while (min <= max) {
                var num = Math.floor(min);
                if (num == 0) {
                    min++;
                    t.push(num);
                    continue;
                }
                if (minInterval <= parent.maxDivXLines || num % tick == 0) {
                    t.push(num);
                }
                min++;
            }

//            calculatePointRadius(this,minInterval);

            return t;
        }
    };

    this.options.yAxis = [
        {
            minorGridLineColor: '#F9F9F9',
            minorTickInterval: 'auto',
            minorGridLineWidth: parent.gridLineWidth,
            title: {
                text: null
            },
            offset: -10,
            labels: {
                useHTML:true,
                formatter: function() {
                    return parent.prefix + parent.render(this.value) + parent.numberSuffix;
                }
            },
            gridLineColor: '#ECEBEB'
        },
        {
            title: {
                text: null
            },
            labels: {
                enabled:false
            },
            gridLineColor: '#ECEBEB',
            gridLineWidth:0
        }
    ];

    this.options.tooltip = {
        useHTML:true,
        crosshairs: {
            color: '#5A5A5A',
            dashStyle:'solid'
        }
        ,
        formatter: function() {
            if (parent.sharedTooltip) {
                var s = this.x + "</br>";
                jQuery.each(this.points, function () {
                    s += '<span style="color:' + this.series.color + '">● </span>' + this.series.name + " ," + parent.prefix + parent.render(this.y) + parent.numberSuffix + ((this.series.index != parent.series.length - 1) ? '<br/>' : '');
                });

                return s;
            }


            return parent.hasDataText ? parent.series[this.series.index].dataText[this.point.index] : ((parent.showSeriesName ? this.series.name + '<br/>' : '') + this.x + '<br/><b>' + parent.checkPrefix(this.series) + parent.render(this.y) + parent.checkSuffix(this.series) + '</b>');
        },
        shared: false,
        animation:false
    };
    this.options.plotOptions = {
        animation: false,
//        column: {
//            borderWidth: 0.01
//        },
        series:
        {
            maxPointWidth: 60,
            connectNulls : true,
            lineWidth:1,
            animation: false,
            marker:
            {
                fillColor: '#FFFFFF',
                lineWidth: 1.3,
                radius : 1.5,
                lineColor: null,
                enabled: false
            },
            states: {
                hover: {
                    enabled: true
                }
            }
        }
    };


    this.setData = function(json) {
        this.initData(json, 0);
        if (hasText(json.SYAxisMaxValue)) {
            if (this.options.series.length != 1) {
                this.options.yAxis[this.options.yAxis.length - 1].max = json.SYAxisMaxValue;
            } else {
                this.options.yAxis[0].max = json.SYAxisMaxValue;
            }
        }
        if (hasText(json.SYAxisMinValue)) {
            this.options.yAxis[this.options.yAxis.length - 1].min = json.SYAxisMinValue;
        }
        if (hasText(json.showMarker) && json.showMarker) {
            this.options.plotOptions.series.marker.enabled = true
        }
        if (hasText(this.categories)) {
            calculatePointRadius(undefined, this.categories.length);
        }
    };

    function calculatePointRadius(chart, interval) {
        if (!isNaN(interval)) {
            if (interval > 100) {
                var radius = 10 * (1 / Math.sqrt(interval));
                parent.options.plotOptions.series.marker.radius = radius;
                if (hasText(chart)) {
                    chart.series[0].update({marker:{radius:radius}});
                }
            } else {
                if (hasText(chart)) {
                    chart.series[0].update({marker:{radius:2}});
                }
                parent.options.plotOptions.series.marker.radius = 2;
            }
        }
    }
}

function StackColumn(divId) {

    this.parent.constructor.call(this, divId);
    var parent = this;

    this.options.xAxis = {
        lineColor: '#ffffff',
        tickColor:'#ffffff',
        categories: [],
        labels: {
            style: {
                fontSize: '9px',
                fontFamily: 'Arial'
            }
        },
        title: {
            style: {
                fontWeight: 'bold',
                color: 'black'
            },
            text: null
        }

    };
    this.options.yAxis = {
        offset: -10,
        minorGridLineColor: '#F9F9F9',
        minorTickInterval: 'auto',
        minorGridLineWidth: 1,
//        min: 0,
        title: {
            text: null
        },
        labels: {
            formatter: function () {
                return  parent.parseAsTime ? parent.duration(this.value) : (parent.categoriesLabels != undefined ? parent.categoriesLabels[parent.categories.indexOf(this.value)] : parent.prefix + parent.render(this.value) + parent.numberSuffix);
            },
            style: {
                fontSize: '9px',
                fontFamily: 'Arial'
            }
        },
        gridLineColor: '#ECEBEB',
        stackLabels: {
            enabled: true,
            style: {
                fontSize: '9px' ,
                fontFamily: 'Tahoma'
            },
            formatter: function() {
                var x1 = 0;
                if (this.axis.series[0].visible) {
                    x1 = parent.series[0].data[this.x];

                }
                var x2 = 0;
                if (this.axis.series[1].visible) {
                    x2 = parent.series[1].data[this.x];

                }

                var delta = x1 + x2;
                if (!this.isNegative) {
                    if (delta >= 0) {
                        return parent.render(delta);
                    } else {
                        return undefined;
                    }
                } else {
                    if (delta < 0) {
                        return parent.render(delta);
                    } else {
                        return undefined;
                    }
                }
            }
        }
    };
    this.options.tooltip = {

        formatter: function () {
            return parent.hasDataText ? parent.series[this.series.index].dataText[this.point.index] : this.series.name + "," + this.x + "," + parent.duration(this.y);
        },
        style: {
            zIndex: 100
        }
    };
    this.options.plotOptions = {
        series: {
            animation: false,

            maxPointWidth: 60,
            stacking: 'normal'
        },
        column: {
            animation:false,
            fillOpacity: 0.5,
            borderWidth: 0,
            dataLabels: {
                enabled: false

            }
        }
    };

    this.options.legend.reversed = true;

    this.setData = function(json) {
        this.initData(json, 0);
    };
}

function ScatterChart(divId) {

    this.parent.constructor.call(this, divId);

    var parent = this;

    this.options.chart = {
        type: 'scatter'    ,
        renderTo: divId
    };
    this.options.xAxis = {
        gridLineColor: '#ECEBEB',
        gridLineWidth:1,
        tickColor:'#ffffff',
        labels: {
            style: {
                fontSize: '11px',
                fontFamily: 'Arial'
            },
            formatter: function () {
                return parent.categoriesLabels != undefined ? parent.categoriesLabels[parent.categories.indexOf(this.value)] : this.value;
            }
        },
        title: {
            style: {
                fontWeight: 'bold',
                color: 'black'
            },
            text: null
        }
    };
    this.options.yAxis = {
        offset: -10,
        minorGridLineColor: '#F9F9F9',
        minorTickInterval: 'auto',
        minorGridLineWidth: 1,
        title: {
            text: null
        },
        gridLineColor: '#ECEBEB',
        stackLabels: {
            enabled: true,
            style: {
                color: 'black'
            }
        },
        labels: {
            style: {
                fontSize: '11px',
                fontFamily: 'Arial'
            },
            formatter: function () {
                return  parent.prefix + parent.render(this.value) + parent.numberSuffix;
            }
        }
    };
    this.options.tooltip = {
        formatter: function () {

            return parent.series[this.series.index].dataText != undefined ? parent.series[this.series.index].dataText[this.point.index] : (this.series.name + "," + this.y);
        },
        style: {
            zIndex: 100
        }
    };
    this.options.plotOptions = {
        animation: false,
        column:{
            animation:false
        },
        scatter: {
            marker: {
                radius: 5,
                states: {
                    hover: {
                        enabled: true,
                        lineColor: 'rgb(100,100,100)'
                    }
                }
            },
            states: {
                hover: {
                    marker: {
                        enabled: false
                    }
                }
            }
        }
    };

    this.options.legend.reversed = true;

    this.setData = function(json) {
        this.initData(json, 1);

    };
}

function highchartsHandleClick(response) {
    eval(response);
}

function ColumnChart(divId) {

    this.parent.constructor.call(this, divId);
    var parent = this;
    this.options.xAxis = {
        lineColor: '#ffffff',
        tickColor:'#ffffff',
        categories: [],
        labels: {
            style: {
                fontSize: '9px',
                fontFamily: 'Arial'
            },
            useHTML:true,
            formatter: function() {
                if (parent.onclickResponse != undefined) {
                    var response = parent.onclickResponse[parent.categories.indexOf(this.value)];

                    return "<span onclick=\"" + response + "\" style='cursor: pointer'>" + this.value + "</span>";
                } else {
                    return  this.value
                }
            },
            title: {
                style: {
                    fontWeight: 'bold',
                    color: 'black'
                },
                text: null
            }
        }
    };
    this.options.yAxis = {
        offset: -10,
        minorGridLineColor: '#F9F9F9',
        minorTickInterval: 'auto',
        minorGridLineWidth: 1,
        title: {
            text: null
        },
        labels: {
            style: {
                fontSize: '9px',
                fontFamily: 'Arial'
            },
            formatter: function() {
                return parent.prefix + parent.render(this.value) + parent.numberSuffix;
            }
        }
        ,
        gridLineColor: '#ECEBEB'
    };
    this.options.tooltip = {
        formatter: function () {
            return (parent.series[0].name != undefined ? parent.series[0].name + "," : "") + this.x + "," + parent.prefix + parent.render(this.y) + parent.numberSuffix;
        },
        style: {
            zIndex: 10000
        }
    };
    this.options.plotOptions = {
        animation: false,
        column: {

            pointPadding: 0,
            borderWidth: 0 ,
            animation:false,
            dataLabels: {
//                useHTML:true,
                style: {
                    fontSize: '9px'

                },
                inside:false,
                enabled: true,
                formatter: function () {
                    return  parent.prefix + this.y + parent.numberSuffix;
                }
            }
        },
        series: {
            animation: false,
            maxPointWidth: 60,
            cursor: 'none',
            point: {
                events: {
                    click: function() {
                        if (parent.onclickResponse != undefined) {
                            eval(parent.onclickResponse[this.index]);
                        }
                    }
                },
                colorByPoint: false
            },
            dataLabels: {
//                useHTML:true,
                style: {
                    fontSize: '9px'

                },
                inside:false,
                enabled: true,
                formatter: function () {
                    return  parent.prefix + this.y + parent.numberSuffix;
                }
            }
        }};


    this.setData = function(json) {
        this.initData(json, 0);

        if (hasText(json.SYAxisMinValue)) {
            if (json.SYAxisMinValue == 0) {
                this.options.yAxis.min = 0;
                this.options.yAxis.max = 1;
            }
        }
    };


}

function PieChart(divId) {

    ChartParent.call(this, divId);
    var parent = this;
    this.options.chart = {
        renderTo: this.divId,
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false
    };

    this.options.tooltip = {
        formatter: function () {
            return this.point.name + " , " + this.point.y;
        }
    };
    this.options.plotOptions = {
        pie: {
            animation: false,
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                distance: 10,
                enabled: true,
                format: '{point.name}: {point.percentage:.1f} %',
                style: {
                    fontSize: '9px',
                    fontFamily: 'Arial'
                }
            }
        }
    };

    this.setData = function(json) {
        this.initData(json, 1);
    };
}


function SimpleLineChart(divId) {

    this.parent.constructor.call(this, divId);
    var parent = this;

    this.options.chart = {
        animation:false,
        renderTo: this.divId,
        plotBorderWidth:0,


        spacingBottom: 0,
        spacingTop: 0,
        spacingLeft: 0,
        spacingRight: 0


    };

    this.options.tooltip = {
        enabled : false
    };

    this.options.xAxis = {
        categories: [] ,
        gridLineColor: '#F2F0F0',
        gridLineWidth:parent.gridLineWidth       ,
        startOnTick:true,
        tickColor:'#ffffff' ,
        lineColor: '#ffffff',
        labels: {
            enabled: false
        },
        //calculate the labels ticks
        tickPositioner: function (min, max) {
            var t = [];
            var minInterval = max - min;
            var tick = Math.floor(minInterval / parent.maxDivXLines);
            while (min <= max) {
                var num = Math.floor(min);
                if (num == 0) {
                    min++;
                    t.push(num);
                    continue;
                }
                if (minInterval <= parent.maxDivXLines || num % tick == 0) {
                    t.push(num);
                }
                min++;
            }
            return t;
        }
    };

    this.options.yAxis = {
        startOnTick: false,
        minPadding: 0.1,
        title: {
            text: null
        },
        labels: {
            enabled:false
        },
        gridLineColor: '#ECEBEB'   ,
        plotLines: [
            {
                zIndex : -1,
                value: 0,
                width: 0.2,
                color: '#808080'
            }
        ],
        //calculate the labels ticks
        tickPositioner: function (min, max) {
            var t = [];
            var minInterval = max - min;
            var tick = Math.floor(minInterval / parent.maxDivYLines);
            while (min <= max) {
                var num = Math.floor(min);
                if (num == 0) {
                    min++;
                    t.push(num);
                    continue;
                }
                if (minInterval <= parent.maxDivXLines || num % tick == 0) {
                    t.push(num);
                }
                min++;
            }
            return t;
        }
    };


    this.options.plotOptions = {
        animation: false,
        series:
        {
            pointPadding: 0,
            groupPadding: 0,
            connectNulls : true,
            lineWidth:1,
            animation: false,
            states: {
                hover: {
                    enabled: false
                }
            },
            marker: {
                enabled: false
            }
        }
    };


    this.setData = function(json) {
        this.initData(json, 0);
    };
}


var CHART_TYPE_LINE_COLUMN = 0;
var CHART_TYPE_STACK_COLUMN = 1;
var CHART_TYPE_SCATTER = 2;
var CHART_TYPE_COLUMN = 3;
var CHART_TYPE_PIE = 4;
var CHART_TYPE_SIMPLE_LINE_CHART = 5;

function Chart(width, height, divId, type, emptyText) {
    var chart = undefined;

    this.divExist = false;
    if (jQuery("#" + divId).isExist()) {
        this.divExist = true;
        if (width!=undefined && height!=undefined) {
            jQuery("#" + divId).width(width).height(height);
        }
    }
    var chartSettings = undefined;

    preRender(emptyText);
    chartsObjects[divId] = this;

    if (hasText(emptyText) && this.divExist) {
        var ch = new PieChart(divId);
        ch.setEmptyMessage(emptyText);
        ch.options.chart.height = height;
        ch.options.chart.width = width;
        chart = new Highcharts.Chart(ch.options);
        showLoading(emptyText);

    }


    this.setDataJson = function(data) {
        loading();
        createObjectSettings();
        chartSettings.setData(data);
        render();
    };


    function loading(emptyText) {
        var noData =  emptyText == undefined ? 'Loading, please wait...' : emptyText;
        chartSettings.setEmptyMessage(noData);
        chart = new Highcharts.Chart(chartSettings.getOptions());
        showLoading(noData)
    }

    function createObjectSettings() {
        chartSettings = new LineColumnChart(divId);
        switch (type) {
            case CHART_TYPE_STACK_COLUMN:
                chartSettings = new StackColumn(divId);
                break;
            case CHART_TYPE_SCATTER :
                chartSettings = new ScatterChart(divId);
                break;
            case CHART_TYPE_COLUMN :
                chartSettings = new ColumnChart(divId);
                break;
            case CHART_TYPE_PIE :
                chartSettings = new PieChart(divId);
                break;
            case CHART_TYPE_SIMPLE_LINE_CHART :
                chartSettings = new SimpleLineChart(divId);
                break;
            default:
                chartSettings = new LineColumnChart(divId);
                break;
        }

    }

    function showLoading(noData){
        if (!(jQuery.browser.msie  && jQuery.browser.version <=8)) {
            chart.showLoading(noData);
        }
    }

    this.renderChart = function(url) {
        if (this.divExist) {
            loading();
            createObjectSettings();
            jQuery.getJSON(url + "&rand=" + Math.random(), function(json) {
                chartSettings.setData(json);
                render();
            });
        }
    };

    function preRender(emptyText) {
        try {
            chart = chartsObjects[divId];
            if (chart != undefined) {
                destroyChart();
            }
        } catch(e) {
        }
        if (chartSettings == undefined) {
            chartSettings = new LineColumnChart(divId);
            chartSettings.options.chart.height = height;
            chartSettings.options.chart.width = width;
        }
        loading(emptyText);
    }

    function render() {

        destroyChart();
        if (chartSettings.isEmpty()) {
            var noData = $T("tNoDataToDisplay");
            chartSettings.setEmptyMessage(noData);
            chart = new Highcharts.Chart(chartSettings.getOptions());
            showLoading(noData);

        } else {
            chart = new Highcharts.Chart(chartSettings.getOptions());
        }
    }

    function destroyChart() {
        try {
            chart.destroy();
        } catch(e) {
        }
    }

    this.getChart = function() {
        return chart;
    }
}
