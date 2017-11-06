(function () {
    'use strict';

    angular
        .module('adist')
        .controller('ProcessController', ProcessController);

    ProcessController.$inject = ['webservice', '$routeParams', '$rootScope', '$location'];

    function ProcessController(webservice, $routeParams, $rootScope, $location) {
        var vm = this;

        vm.isGraphLoaderVisible = true;
        vm.isResultVisible = false;
        vm.onEntropyHover = false;
        vm.isOrderBookLoaded = false;

        vm.loadData = loadData;
        vm.selectData = selectData;
        vm.changeGraph = changeGraph;
        vm.getPreviousWindow = getPreviousWindow;
        vm.getNextWindow = getNextWindow;

        console.log("Process Controller");

        vm.id = $routeParams.id;
        vm.time_frame_number = 13;
        vm.entropy_score = 3;
        vm.local_minima_list = [];
        vm.current_file = 0;
        vm.files_range = [];

        initialize();

        function initialize() {
            var os = $location.search().orderbook_simulation;

            if (os == "true") {
                vm.isOrderBookLoaded = true;
                // webservice.call('/process_main/simulate_orderbook', 'post').then(function () {
                setTimeout(function () {
                    alert("Hello");
                }, 10000);
                // });
            }

            vm.loadData(vm.id);
        }

        function loadData(id) {
            var data = {
                id: id
            };

            webservice.call('/process_main/get_data', 'post', JSON.stringify(data)).then(function (response) {
                console.log(response.data);

                createEntropyGraph(response.data);

                vm.files_count = parseInt(response.data.files_count);
                vm.current_file = parseInt(response.data.max_anomalous_file);
                updateFilesRange(vm.files_count);

                var local_minimas = response.data.local_minimas;

                angular.forEach(local_minimas, function (value, key) {
                    var time = response.data.time_index[value];
                    time = time.split('$$');

                    var starttime = time[1];
                    var endtime = time[2];

                    vm.local_minima_list.push({
                        entropy_value: response.data.entropy_exec_type[value],
                        id: (value + 1),
                        starttime: starttime,
                        endtime: endtime
                    });
                });

                vm.selectData(vm.current_file);
            });
        }

        function changeGraph() {
            console.log("Curent file is: " + vm.current_file);
            selectData(vm.current_file);
        }

        function selectData(file_number) {
            vm.isGraphLoaderVisible = true;

            var data = {
                id: vm.id,
                file_number: file_number
            };

            webservice.call('/process_main/select_data', 'post', JSON.stringify(data)).then(function (response) {
                console.log(response.data);

                vm.isLoaderVisible = false;
                vm.isResultVisible = true;

                createAttributeGraph(response.data, file_number);
            });
        }

        function getNextWindow() {
            vm.current_file++;

            selectData(vm.current_file)
        }

        function getPreviousWindow() {
            vm.current_file--;

            selectData(vm.current_file)
        }

        function createEntropyGraph(values) {
            var dataset = [];

            for (var i = 0; i < Object.keys(values.time_index).length; i++) {
                dataset.push({
                    ax: (i + 1),
                    ay: values.entropy_exec_type[i]
                });
            }

            var chart = AmCharts.makeChart("entropy-linechart", {
                "type": "xy",
                "theme": "light",
                "marginRight": 80,
                "dataDateFormat": "YYYY-MM-DD",
                "startDuration": 0,
                "trendLines": [],
                "balloon": {
                    "adjustBorderColor": false,
                    "shadowAlpha": 0,
                    "fixedPosition": true
                },
                "graphs": [{
                    "balloonText": "<div style='margin:5px;'><b>[[x]]</b><br>y:<b>[[y]]</b></div>",
                    "bullet": "diamond",
                    "maxBulletSize": 25,
                    "lineAlpha": 0.8,
                    "lineThickness": 2,
                    "lineColor": "#b0de09",
                    "fillAlphas": 0,
                    "xField": "ax",
                    "yField": "ay",
                    "valueField": "aValue"
                }],
                "valueAxes": [{
                    "id": "ValueAxis-1",
                    "axisAlpha": 0
                }],
                "allLabels": [],
                "titles": [],
                "dataProvider": dataset,

                "export": {
                    "enabled": true
                },

                "chartScrollbar": {
                    "offset": 15,
                    "scrollbarHeight": 5
                },

                "chartCursor": {
                    "pan": true,
                    "cursorAlpha": 0,
                    "valueLineAlpha": 0
                }
            });
        }

        function createAttributeGraph(values, file_number) {
            var dataset = [];
            for (var i = 0; i < Object.keys(values.time_index).length; i++) {
                dataset.push({
                    date: values.time_index[i],
                    value: values.nom_price_gap[i]
                });
            }

            var chart = AmCharts.makeChart("price-gap-linechart", {
                "type": "serial",
                "theme": "light",
                "marginRight": 40,
                "marginLeft": 40,
                "autoMarginOffset": 20,
                "mouseWheelZoomEnabled": true,
                "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
                "valueAxes": [{
                    "id": "v1",
                    "axisAlpha": 0,
                    "position": "left",
                    "ignoreAxisWidth": true
                }],
                "balloon": {
                    "borderThickness": 1,
                    "shadowAlpha": 0
                },
                "graphs": [{
                    "id": "g1",
                    "balloon": {
                        "drop": true,
                        "adjustBorderColor": false,
                        "color": "#ffffff"
                    },
                    "bullet": "round",
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "bulletSize": 5,
                    "hideBulletsCount": 50,
                    "lineThickness": 2,
                    "title": "red line",
                    "useLineColorForBulletBorder": true,
                    "valueField": "value",
                    "balloonText": "<span style='font-size:18px;'>[[value]]</span>"
                }],
                "chartScrollbar": {
                    "graph": "g1",
                    "oppositeAxis": false,
                    "offset": 30,
                    "scrollbarHeight": 80,
                    "backgroundAlpha": 0,
                    "selectedBackgroundAlpha": 0.1,
                    "selectedBackgroundColor": "#888888",
                    "graphFillAlpha": 0,
                    "graphLineAlpha": 0.5,
                    "selectedGraphFillAlpha": 0,
                    "selectedGraphLineAlpha": 1,
                    "autoGridCount": true,
                    "color": "#AAAAAA"
                },
                "chartCursor": {
                    "pan": true,
                    "valueLineEnabled": true,
                    "valueLineBalloonEnabled": true,
                    "cursorAlpha": 1,
                    "cursorColor": "#258cbb",
                    "limitToGraph": "g1",
                    "valueLineAlpha": 0.2,
                    "valueZoomable": true
                },
                "valueScrollbar": {
                    "oppositeAxis": false,
                    "offset": 50,
                    "scrollbarHeight": 10
                },
                "categoryField": "date",
                "categoryAxis": {
                    "parseDates": false,
                    "dashLength": 1,
                    "minorGridEnabled": true
                },
                "export": {
                    "enabled": true
                },
                "dataProvider": dataset
            });

            vm.isGraphLoaderVisible = false;
        }

        function updateFilesRange(n) {
            vm.files_range = [];
            for (var i = 1; i <= n; i++) {
                vm.files_range.push(i);
            }
        }
    }
})();