(function () {
    'use strict';

    angular
        .module('adist')
        .controller('ProcessController', ProcessController);

    ProcessController.$inject = ['webservice', '$routeParams'];

    function ProcessController(webservice, $routeParams) {
        var vm = this;

        vm.isLoaderVisible = true;
        vm.isResultVisible = false;

        console.log("Process Controller");

        vm.id = $routeParams.id;


    }
})();