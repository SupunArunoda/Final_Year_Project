(function () {
    'use strict';

    // Declare app level module which depends on views, and components
    angular
        .module('adist', ['ngRoute', 'angularFileUpload'])

        .config(function ($routeProvider, $locationProvider) {
            $routeProvider
                .when('/preprocess', {
                    templateUrl: 'components/preprocess.html',
                    controller: 'PreprocessController',
                    controllerAs: 'vm'
                })

                // By default it will open /
                .otherwise({redirectTo: '/'});

            // $locationProvider.html5Mode(true);
        });
})();
