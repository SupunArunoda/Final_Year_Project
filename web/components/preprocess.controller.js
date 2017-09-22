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

        vm.testFunction = testFunction;
        vm.uploadFile = uploadFile;
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

        function uploadFile() {
            vm.isLoaderVisible = true;

            var fileFormData = new FormData();
            fileFormData.append('inputFile', fileservice[0]);

            webservice.call('/preprocess_main/get_csv_information', 'post', fileFormData).then(function (response) {
                console.log(response.data);

                vm.isResultVisible = true;
                vm.isLoaderVisible = false;

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

                var data = [{
                    values: response.data.piechart_sizes,
                    labels: response.data.piechart_labels,
                    type: 'pie'
                }];
                var layout = {
                    height: '100%',
                    width: '100%'
                };
                Plotly.newPlot('order-count-piechart', data, layout);
            });
        }

        function processFile() {
            vm.isProcessLoaderVisible = true;

            var file = fileservice[0];

            var data = {
                file_name: file.name
            };

            webservice.call('/preprocess_main/process', 'post', JSON.stringify(data)).then(function (response) {
                vm.isProcessLoaderVisible = false;

                console.log(response.data);

                $location.path('/process/' + response.data);
            });
        }

        function getStyleForProgressBar(value) {
            return {"width": value + '%'}
        }

        function testFunction() {
            console.log(vm.type);
        }
    }
})();