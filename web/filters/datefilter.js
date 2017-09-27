(function () {
    'use strict';

    angular.module('adist')
        .filter('getstartdate', getstartdate)
        .filter('getenddate', getenddate);

    getstartdate.$inject = [];

    function getstartdate() {
        return function (datestring) {
            var strings = datestring.split('$$');
            return strings[0];
        }
    }

    getenddate.$inject = [];

    function getenddate() {
        return function (datestring) {
            var strings = datestring.split('$$');
            return strings[1];
        }
    }
})();