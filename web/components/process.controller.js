(function () {
    'use strict';

    angular
        .module('adist')
        .controller('ProcessController', ProcessController);

    ProcessController.$inject = ['webservice', '$routeParams', '$rootScope'];

    function ProcessController(webservice, $routeParams, $rootScope) {
        var vm = this;

        vm.isGraphLoaderVisible = true;
        vm.isResultVisible = false;
        vm.onEntropyHover = false;

        vm.loadData = loadData;
        vm.selectData = selectData;
        vm.getPreviousWindow = getPreviousWindow;
        vm.getNextWindow = getNextWindow;

        console.log("Process Controller");

        vm.id = $routeParams.id;
        vm.time_frame_number = 13;
        vm.entropy_score = 3;
        vm.local_minima_list = [];

        vm.loadData(vm.id);

        function loadData(id) {
            var data = {
                id: id
            };

            webservice.call('/process_main/get_data', 'post', JSON.stringify(data)).then(function (response) {
                console.log(response.data);

                createEntropyGraph(response.data);

                vm.files_count = parseInt(response.data.files_count);
                vm.current_file = parseInt(response.data.max_anomalous_file);

                var local_minimas = response.data.local_minimas;

                angular.forEach(local_minimas, function (value, key) {
                    vm.local_minima_list.push({
                        entropy_value: response.data.entropy_exec_type[value],
                        id: (value + 1),
                    });
                });

                vm.selectData(vm.current_file);
            });
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
            var trace = {
                x: values.time_index,
                y: values.entropy_exec_type,
                mode: 'lines+markers',
                marker: {
                    size: 5
                },
                line: {
                    width: 1
                }
            };

            var data = [trace];

            var layout = {
                height: '100%',
                width: '100%'
            };

            Plotly.newPlot('entropy-linechart', data, layout);

            var plot_div = document.getElementById('entropy-linechart');
            plot_div.on('plotly_click', function (data) {
                vm.time_frame_number = parseInt(data.points[0].x);
                vm.entropy_score = data.points[0].y;

                $rootScope.$digest();
                vm.onEntropyHover = true;
            });
        }

        function createAttributeGraph(values, file_number) {
            var trace = {
                y: values.nom_price_gap,
                mode: 'lines+markers',
                marker: {
                    size: 5
                },
                line: {
                    width: 1
                }
            };

            var data = [trace];

            var layout = {
                autosize: false,
                height: '400',
                width: '1000',
                margin: {
                    l: 50,
                    r: 50,
                    b: 50,
                    t: 100,
                    pad: 4
                },
                xaxis: {
                    showline: false,
                    tickvals: Object.keys(values.nom_price_gap),
                    ticktext: '',
                    showticklabels: false,
                    showgrid: false,
                },
                title: 'Time Window ' + file_number + ' of ' + vm.files_count
            };

            vm.isGraphLoaderVisible = false;

            Plotly.newPlot('price-gap-linechart', data, layout);
        }
    }
})();