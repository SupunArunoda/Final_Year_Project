(function () {
    'use strict';

    angular
        .module('adist')
        .controller('ProcessController', ProcessController);

    ProcessController.$inject = ['webservice', '$routeParams', '$rootScope', '$location', '$scope'];

    function ProcessController(webservice, $routeParams, $rootScope, $location, $scope) {
        console.log("Process Controller");

        var vm = this;

        vm.isGraphLoaderVisible = true;
        vm.isResultVisible = false;
        vm.onEntropyHover = false;
        vm.isOrderBookLoaded = false;
        vm.orderbook_simulation = false;
        vm.price_gap_details_show = false;
        vm.broker_details_show = false;
        vm.timeframe_details_show = false;

        vm.loadData = loadData;
        vm.selectData = selectData;
        vm.changeGraph = changeGraph;
        vm.getPreviousWindow = getPreviousWindow;
        vm.getNextWindow = getNextWindow;
        vm.updateOrderBook = updateOrderBook;
        vm.showBrokerModel = showBrokerModel;

        console.log("Process Controller");

        vm.id = $routeParams.id;
        vm.time_frame_number = 13;
        vm.entropy_score = 3;
        vm.local_minima_list = [];
        vm.current_file = 0;
        vm.files_range = [];
        vm.time_point = 0;
        vm.current_orderbook_time = '';
        vm.buy_points = [];
        vm.sell_points = [];

        vm.clicked_price_gap_value = '';
        vm.clicked_price_gap_from = '';
        vm.clicked_price_gap_to = '';
        vm.clicked_start_broker = '';
        vm.clicked_end_broker = '';

        vm.current_selected_broker = '';
        vm.broker_orders_count = '';
        vm.selected_timeframe = '';
        vm.selected_timeframe_start = '';
        vm.selected_timeframe_end = '';

        vm.timeframe_orders_count = '';
        vm.timeframe_new_orders_count = '';
        vm.timeframe_cancel_orders_count = '';
        vm.timeframe_ammend_orders_count = '';
        vm.timeframe_execute_orders_count = '';

        initialize();

        function initialize() {

            if ($location.search().orderbook_simulation == "false") {
                vm.orderbook_simulation = false;
            } else {
                vm.orderbook_simulation = true;
            }
            vm.loadData(vm.id);
        }

        function loadData(id) {
            var data = {
                id: id
            };

            webservice.call('/process_main/get_data', 'post', JSON.stringify(data)).then(function (response) {
                console.log(response.data);

                var max_anomaly_score = response.data.anomaly_score.reduce(function (a, b) {
                    return Math.max(a, b);
                });

                vm.timeframes_list = [];
                vm.max_anomalous_list = [];
                for (var i = 0; i < response.data.files_count; i++) {
                    var time = response.data.time_index[i];
                    time = time.split('000$$');

                    var starttime = time[0];
                    var endtime = time[1];

                    vm.timeframes_list.push({
                        timeframe_index: i + 1,
                        timeframe_entropy_value: response.data.anomaly_score[i],
                        timeframe_start: starttime,
                        timeframe_end: endtime
                    });

                    if (response.data.anomaly_score[i] == max_anomaly_score.toString()) {
                        vm.max_anomalous_list.push({
                            timeframe_index: i + 1,
                            timeframe_anomaly_score: response.data.anomaly_score[i],
                            timeframe_start: starttime,
                            timeframe_end: endtime
                        });
                    }
                }

                createEntropyGraph(response.data);
                createClusteringGraph(response.data)

                vm.files_count = parseInt(response.data.files_count);
                vm.current_file = parseInt(response.data.max_anomalous_file);
                updateFilesRange(vm.files_count);

                var local_minimas = response.data.local_minimas;

                angular.forEach(local_minimas, function (value, key) {
                    var time = response.data.time_index[value];
                    time = time.split('000$$');

                    var starttime = time[0];
                    var endtime = time[1];

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
            vm.price_gap_details_show = false;

            var data = {
                id: vm.id,
                file_number: file_number
            };

            webservice.call('/process_main/select_data', 'post', JSON.stringify(data)).then(function (response) {
                console.log(response.data);

                vm.isLoaderVisible = false;
                vm.isResultVisible = true;

                createAttributeGraph(response.data.price_gap_data, file_number);
                updateOrderbookTable(response.data.orderbook_data)

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
                    "balloonText": "<div style='margin:5px;'><b>Timeframe [[x]]</b><br><b>[[y]]</b></div>",
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
                },
                "listeners": [{
                    "event": "clickGraphItem",
                    "method": (function (e) {
                        $('#timeframe-modal').modal({
                            backdrop: 'static',
                            keyboard: true,
                            show: true
                        });

                        vm.timeframe_details_show = false;
                        vm.selected_timeframe = e.item.dataContext.ax;

                        vm.selected_timeframe_start = vm.timeframes_list[vm.selected_timeframe - 1].timeframe_start;
                        vm.selected_timeframe_end = vm.timeframes_list[vm.selected_timeframe - 1].timeframe_end;

                        var data = {
                            id: vm.id,
                            file_id: vm.selected_timeframe
                        };

                        webservice.call('/process_main/get_timeframe_data', 'post', JSON.stringify(data)).then(function (response) {
                            console.log(response.data);

                            vm.timeframe_orders_count = response.data.all;
                            vm.timeframe_new_orders_count = response.data.new;
                            vm.timeframe_cancel_orders_count = response.data.cancel;
                            vm.timeframe_ammend_orders_count = response.data.ammend;
                            vm.timeframe_execute_orders_count = response.data.execute;

                            vm.timeframe_traders_details_all = response.data.sortedAll;
                            vm.timeframe_traders_details_new = response.data.sortedNew;
                            vm.timeframe_traders_details_execute = response.data.sortedExecute;
                            vm.timeframe_traders_details_cancel = response.data.sortedCancel;
                            vm.timeframe_traders_details_ammend = response.data.sortedAmmend;

                            var dataset = [{
                                "type": "New Orders",
                                "count": response.data.new
                            }, {
                                "type": "Cancelled Orders",
                                "count": response.data.cancel
                            }, {
                                "type": "Ammended Orders",
                                "count": response.data.ammend
                            }, {
                                "type": "Executed Orders",
                                "count": response.data.execute
                            }];

                            var chart = AmCharts.makeChart("timeframe-order-count-piechart", {
                                "type": "pie",
                                "theme": "light",
                                "dataProvider": dataset,
                                "startDuration": 0,
                                "valueField": "count",
                                "titleField": "type",
                                "balloon": {
                                    "fixedPosition": true
                                },
                                "export": {
                                    "enabled": true
                                }
                            });

                            vm.timeframe_details_show = true;
                        });

                        $scope.$apply();
                    }).bind(vm)
                }]
            });
        }

        function createClusteringGraph(values) {
            var dataset = [];

            for (var i = 0; i < Object.keys(values.time_index).length; i++) {
                dataset.push({
                    ax: (i + 1),
                    ay: values.anomaly_score[i]
                });
            }

            var chart = AmCharts.makeChart("clustering-linechart", {
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
                    "balloonText": "<div style='margin:5px;'><b>Timeframe [[x]]</b><br><b>[[y]]</b></div>",
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
                },
                "listeners": [{
                    "event": "clickGraphItem",
                    "method": (function (e) {
                        $('#timeframe-modal').modal({
                            backdrop: 'static',
                            keyboard: true,
                            show: true
                        });

                        vm.timeframe_details_show = false;
                        vm.selected_timeframe = e.item.dataContext.ax;

                        vm.selected_timeframe_start = vm.timeframes_list[vm.selected_timeframe - 1].timeframe_start;
                        vm.selected_timeframe_end = vm.timeframes_list[vm.selected_timeframe - 1].timeframe_end;

                        var data = {
                            id: vm.id,
                            file_id: vm.selected_timeframe
                        };

                        webservice.call('/process_main/get_timeframe_data', 'post', JSON.stringify(data)).then(function (response) {
                            console.log(response.data);

                            vm.timeframe_orders_count = response.data.all;
                            vm.timeframe_new_orders_count = response.data.new;
                            vm.timeframe_cancel_orders_count = response.data.cancel;
                            vm.timeframe_ammend_orders_count = response.data.ammend;
                            vm.timeframe_execute_orders_count = response.data.execute;

                            vm.timeframe_traders_details_all = response.data.sortedAll;
                            vm.timeframe_traders_details_new = response.data.sortedNew;
                            vm.timeframe_traders_details_execute = response.data.sortedExecute;
                            vm.timeframe_traders_details_cancel = response.data.sortedCancel;
                            vm.timeframe_traders_details_ammend = response.data.sortedAmmend;

                            var dataset = [{
                                "type": "New Orders",
                                "count": response.data.new
                            }, {
                                "type": "Cancelled Orders",
                                "count": response.data.cancel
                            }, {
                                "type": "Ammended Orders",
                                "count": response.data.ammend
                            }, {
                                "type": "Executed Orders",
                                "count": response.data.execute
                            }];

                            var chart = AmCharts.makeChart("timeframe-order-count-piechart", {
                                "type": "pie",
                                "theme": "light",
                                "dataProvider": dataset,
                                "startDuration": 0,
                                "valueField": "count",
                                "titleField": "type",
                                "balloon": {
                                    "fixedPosition": true
                                },
                                "export": {
                                    "enabled": true
                                }
                            });

                            vm.timeframe_details_show = true;
                        });

                        $scope.$apply();
                    }).bind(vm)
                }]
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
                "showBalloon": "false",
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
                "dataProvider": dataset,
                "listeners": [{
                    "event": "clickGraphItem",
                    "method": (function (e) {
                        vm.clicked_price_gap_value = values.nom_price_gap[e.index];
                        vm.clicked_start_broker = values.start_broker[e.index];
                        vm.clicked_end_broker = values.end_broker[e.index];

                        var clicked_price_gap_time = values.time_index[e.index].split("$$");
                        vm.clicked_price_gap_from = clicked_price_gap_time[0];
                        vm.clicked_price_gap_to = clicked_price_gap_time[1];

                        vm.price_gap_details_show = true;
                        $scope.$apply();
                    }).bind(vm)
                }]
            });

            // chart.addListener("clickGraphItem", priceGapClickEvent().bind(this));

            vm.isGraphLoaderVisible = false;
        }

        function priceGapClickEvent(e) {
            console.log("asdbhasd");
            console.log(e);
        }

        function updateOrderbookTable(values) {
            console.log(values);

            if (values == null) {
                vm.isOrderBookLoaded = false;
            } else {
                vm.orderbook_data = [];

                angular.forEach(values, function (value, key) {
                    var bp = value[3].split(",");
                    var sp = value[4].split(",");

                    vm.orderbook_data.push({
                        time_point: value[2].split("000$$")[0],
                        buy_points: bp.slice(0, bp.length - 1),
                        sell_points: sp.slice(0, bp.length - 1)
                    });
                });
                vm.orderbook_data.time_points_count = Object.keys(vm.orderbook_data).length;
                vm.current_orderbook_time = vm.orderbook_data[0];
                vm.buy_points = vm.orderbook_data[0].buy_points;
                vm.sell_points = vm.orderbook_data[0].sell_points;

                vm.isOrderBookLoaded = true;
            }

        }

        function updateFilesRange(n) {
            vm.files_range = [];
            for (var i = 1; i <= n; i++) {
                vm.files_range.push(i);
            }
        }

        function updateOrderBook() {
            vm.current_orderbook_time = vm.orderbook_data[vm.time_point];

            vm.buy_points = vm.orderbook_data[vm.time_point].buy_points;
            vm.sell_points = vm.orderbook_data[vm.time_point].sell_points;
        }

        function showBrokerModel(broker_id, file_id) {
            console.log(broker_id);
            vm.broker_details_show = false;
            vm.broker_orders_count = '';
            vm.broker_new_orders_count = '';
            vm.broker_cancel_orders_count = '';
            vm.broker_ammend_orders_count = '';
            vm.broker_execute_orders_count = '';

            $('#broker-modal').modal({
                backdrop: 'static',
                keyboard: true,
                show: true
            });
            vm.current_selected_broker = broker_id;
            vm.broker_details_show = false;

            var data = {
                broker_id: broker_id,
                file_id: file_id,
                id: vm.id
            };

            webservice.call('/process_main/get_broker_data', 'post', JSON.stringify(data)).then(function (response) {
                console.log(response.data);

                vm.broker_orders_count = response.data.order_count;
                vm.broker_new_orders_count = response.data.order_types_count.new;
                vm.broker_cancel_orders_count = response.data.order_types_count.cancel;
                vm.broker_ammend_orders_count = response.data.order_types_count.ammend;
                vm.broker_execute_orders_count = response.data.order_types_count.execute;

                var dataset = [{
                    "type": "New Orders",
                    "count": response.data.order_types_count.new
                }, {
                    "type": "Cancelled Orders",
                    "count": response.data.order_types_count.cancel
                }, {
                    "type": "Ammended Orders",
                    "count": response.data.order_types_count.ammend
                }, {
                    "type": "Executed Orders",
                    "count": response.data.order_types_count.execute
                }];

                var chart = AmCharts.makeChart("broker-order-count-piechart", {
                    "type": "pie",
                    "theme": "light",
                    "dataProvider": dataset,
                    "startDuration": 0,
                    "valueField": "count",
                    "titleField": "type",
                    "balloon": {
                        "fixedPosition": true
                    },
                    "export": {
                        "enabled": true
                    }
                });

                var dataset = [];

                for (var i = 0; i < response.data.order_count; i++) {
                    var temp = {
                        date: response.data.orders[i][9],
                    };
                    if (response.data.orders[i][3] == 0) {
                        temp.value1 = 1
                    } else if (response.data.orders[i][3] == 4) {
                        temp.value2 = 2
                    } else if (response.data.orders[i][3] == 5) {
                        temp.value3 = 3
                    } else if (response.data.orders[i][3] == 15) {
                        temp.value4 = 4
                    }
                    dataset.push(temp);
                }

                var chart = AmCharts.makeChart("broker-order-placement-graph", {
                    "type": "serial",
                    "theme": "light",
                    "marginRight": 70,
                    "autoMarginOffset": 20,
                    "dataProvider": dataset,
                    "balloon": {
                        "cornerRadius": 6
                    },
                    "valueAxes": [{
                        "axisAlpha": 0,
                        "labelsEnabled": false
                    }],
                    "graphs": [{
                        "balloonText": "[[category]]<br><b><span style='font-size:14px;'>NEW</span></b>",
                        "bullet": "round",
                        "bulletSize": 2,
                        "connect": false,
                        "lineColor": "#d2742a",
                        "lineThickness": 1,
                        "negativeLineColor": "#487dac",
                        "valueField": "value1"
                    }, {
                        "balloonText": "[[category]]<br><b><span style='font-size:14px;'>CANCEL</span></b>",
                        "bullet": "round",
                        "bulletSize": 2,
                        "connect": false,
                        "lineColor": "#3734d2",
                        "lineThickness": 1,
                        "negativeLineColor": "#ac0023",
                        "valueField": "value2"
                    }, {
                        "balloonText": "[[category]]<br><b><span style='font-size:14px;'>AMMEND</span></b>",
                        "bullet": "round",
                        "bulletSize": 2,
                        "connect": false,
                        "lineColor": "#d258d2",
                        "lineThickness": 1,
                        "negativeLineColor": "#ac0023",
                        "valueField": "value3"
                    }, {
                        "balloonText": "[[category]]<br><b><span style='font-size:14px;'>EXECUTE</span></b>",
                        "bullet": "round",
                        "bulletSize": 2,
                        "connect": false,
                        "lineColor": "#7fd21b",
                        "lineThickness": 1,
                        "negativeLineColor": "#ac0023",
                        "valueField": "value4"
                    }],
                    "chartCursor": {
                        "categoryBalloonDateFormat": "YYYY-MM-DD HH:NN:SS",
                        "cursorAlpha": 0.1,
                        "cursorColor": "#000000",
                        "fullWidth": true,
                        "graphBulletSize": 2
                    },
                    "chartScrollbar": {},
                    "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
                    "categoryField": "date",
                    "categoryAxis": {
                        "minPeriod": "YYYY-MM-DD HH:NN:SS",
                        "parseDates": false,
                        "minorGridEnabled": true
                    },
                    "export": {
                        "enabled": true
                    }
                });

                vm.broker_details_show = true;

                // $scope.$apply();
            });
        }
    }
})();