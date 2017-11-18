(function () {
    'use strict';

    angular
        .module('adist')
        .controller('PreprocessController', PreprocessController);

    PreprocessController.$inject = ['webservice', 'fileservice', '$location'];

    function PreprocessController(webservice, fileservice, $location) {
        var vm = this;

        console.log('Preprocess Controller');

        vm.isResultVisible = false;
        vm.isLoaderVisible = false;
        vm.isProcessLoaderVisible = false;
        vm.isSessionsUploaded = false;
        vm.orderbookSimulation = false;
        vm.saveInformation = false;

        vm.testFunction = testFunction;
        vm.uploadDataFile = uploadDataFile;
        vm.uploadSessionsFile = uploadSessionsFile;
        vm.processFile = processFile;
        vm.getStyleForProgressBar = getStyleForProgressBar;

        vm.type = null;
        vm.windowSize = null;
        vm.timeInterval = null;

        vm.results = false;
        vm.total_rows = '';
        vm.new_orders_count = '';
        vm.cancel_orders_count = '';
        vm.ammend_orders_count = '';
        vm.execute_orders_count = '';

        vm.new_orders_percentage = '';
        vm.cancel_orders_percentage = '';
        vm.ammend_orders_percentage = '';
        vm.new_orders_percentage = '';

        function uploadSessionsFile() {
            vm.isSessionUploadLoaderVisible = true;

            var fileFormData = new FormData();
            fileFormData.append('sessionsFile', fileservice[0]);

            webservice.call('/preprocess_main/set_session_information', 'post', fileFormData).then(function (response) {
                console.log(response.data);

                vm.isSessionsUploaded = true;
                vm.isSessionUploadLoaderVisible = false;

                var dataset = [{
                    category: 'Sessions',
                    segments: []
                }];
                var colors = ['#FF1800', '#0012FF', '#36FF00', '#EF49FF', '#5FFCFF', '#000000', '#FFFF65', '#FFB417', '#FFA19B'];
                angular.forEach(response.data.session_data, function (value, key) {
                    dataset[0].segments.push({
                        "start": value[1],
                        "end": value[2],
                        "color": colors[key],
                        "task": value[0]
                    });
                });

                console.log(dataset);

                var chart = AmCharts.makeChart("sessions-ganttchart", {
                    "type": "gantt",
                    "theme": "light",
                    "marginRight": 70,
                    "period": "fff",
                    "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
                    "columnWidth": 1,
                    "valueAxis": {
                        "type": "date",
                        "minPeriod": "fff",
                        "ignoreAxisWidth": true
                    },
                    "brightnessStep": 7,
                    "graph": {
                        "fillAlphas": 1,
                        "lineAlpha": 1,
                        "lineColor": "#fff",
                        "balloonText": "<b>[[task]]</b>:<br />[[open]] -- [[value]]"
                    },
                    "rotate": true,
                    "categoryField": "category",
                    "segmentsField": "segments",
                    "colorField": "color",
                    "startDateField": "start",
                    "endDateField": "end",
                    "dataProvider": dataset,
                    "valueScrollbar": {
                        "autoGridCount": true
                    },
                    "chartCursor": {
                        "cursorColor": "#55bb76",
                        "valueBalloonsEnabled": false,
                        "cursorAlpha": 0,
                        "valueLineAlpha": 0.5,
                        "valueLineBalloonEnabled": true,
                        "valueLineEnabled": true,
                        "zoomable": false,
                        "valueZoomable": true
                    },
                    "export": {
                        "enabled": true
                    }
                });

            }).catch(function (err) {
                alert("Server Error!");

                vm.isSessionsUploaded = false;
                vm.isSessionUploadLoaderVisible = false;
            });
        }

        function uploadDataFile() {
            vm.isDataUploadLoaderVisible = true;

            var fileFormData = new FormData();
            fileFormData.append('inputFile', fileservice[Object.keys(fileservice).length - 1]);

            webservice.call('/preprocess_main/get_csv_information', 'post', fileFormData).then(function (response) {
                console.log(response.data);

                vm.isResultVisible = true;
                vm.isDataUploadLoaderVisible = false;

                vm.results = true;
                vm.total_rows = response.data.total_rows;
                vm.new_orders_count = response.data.new_orders_count;
                vm.cancel_orders_count = response.data.cancel_orders_count;
                vm.ammend_orders_count = response.data.ammend_orders_count;
                vm.execute_orders_count = response.data.execute_orders_count;

                vm.new_orders_percentage = response.data.new_orders_percentage + '%';
                vm.cancel_orders_percentage = response.data.cancel_orders_percentage + '%';
                vm.ammend_orders_percentage = response.data.ammend_orders_percentage + '%';
                vm.execute_orders_percentage = response.data.execute_orders_percentage + '%';

                var dataset = [{
                    "type": "New Orders",
                    "count": vm.new_orders_count
                }, {
                    "type": "Cancelled Orders",
                    "count": vm.cancel_orders_count
                }, {
                    "type": "Ammended Orders",
                    "count": vm.ammend_orders_count
                }, {
                    "type": "Executed Orders",
                    "count": vm.execute_orders_count
                }];


                var chart = AmCharts.makeChart("order-count-piechart", {
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
            });
        }

        function processFile() {
            if (vm.type === null) {
                alert('Select processing type to continue');
            } else {
                var window = 0;

                if (vm.type == 'order') {
                    window = vm.windowSize
                } else if (vm.type == 'time') {
                    window = vm.timeInterval;
                }

                if (window == null) {
                    alert('Enter valid value');
                } else {
                    vm.isProcessLoaderVisible = true;

                    var sessionfile = fileservice[0];
                    var datafile = fileservice[1];

                    var data = {
                        session_filename: sessionfile.name,
                        data_filename: datafile.name,
                        type: vm.type,
                        window: window,
                        save_information: vm.saveInformation,
                        orderbook_simulation: vm.orderbookSimulation
                    };

                    webservice.call('/preprocess_main/process', 'post', JSON.stringify(data)).then(function (response) {
                        vm.isProcessLoaderVisible = false;

                        console.log(response.data);

                        // $location.path('/process/' + response.data.proprocess_index);
                        $location.path('/process/' + response.data.proprocess_index).search({
                            // $location.path('/process/101').search({
                            orderbook_simulation: vm.orderbookSimulation
                        });
                    });
                }
            }

            console.log(vm.orderbookSimulation);
            console.log(vm.saveInformation);
        }

        function getStyleForProgressBar(value) {
            return {"width": value + '%'}
        }

        function testFunction() {
            console.log(vm.type);
        }
    }
})();