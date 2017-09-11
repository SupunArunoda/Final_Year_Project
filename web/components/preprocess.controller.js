(function () {
    'use strict';

    angular
        .module('adist')
        .controller('PreprocessController', PreprocessController);

    PreprocessController.$inject = ['webservice', 'fileservice'];

    function PreprocessController(webservice, fileservice) {
        var vm = this;

        console.log('Preprocess Controller');

        vm.isResultVisible = false;

        vm.testFunction = testFunction;
        vm.uploadFile = uploadFile;
        vm.getStyleForProgressBar = getStyleForProgressBar;
        vm.type = null;


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
            var fileFormData = new FormData();
            fileFormData.append('inputFile', fileservice[0]);

            vm.isResultVisible = false;

            webservice.call('/preprocess_main', 'post', fileFormData).then(function (response) {
                console.log(response);

                vm.isResultVisible = true;

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

        function getStyleForProgressBar(value) {
            return {"width": value + '%'}
        }

        function testFunction() {
            console.log(vm.type);
        }
    }
})();