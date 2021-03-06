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
                .when('/process/:id', {
                    templateUrl: 'components/process.html',
                    controller: 'ProcessController',
                    controllerAs: 'vm'
                })

                // By default it will open /
                .otherwise({redirectTo: '/'});

            $locationProvider.hashPrefix('');
        });
})();
