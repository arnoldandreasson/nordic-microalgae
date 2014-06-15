/*
 Nordic Microalgae Mobile. http://m.nordicmicroalgae.org

 Author: Andreas Loo, info@andreasloo.se
 Copyright (c) 2013 SMHI, Swedish Meteorological and Hydrological Institute
 License: MIT License as follows:

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
*/

/*global angular*/
'use strict';

angular.module('nma.services').
  factory('Query', ['$rootScope', 'storage', function($rootScope, storage) {
    var STORAGE_KEY = 'taxon-query';

    var query = angular.extend(storage.get(STORAGE_KEY), {
      page: 1,
      per_page: 50
    });

    $rootScope.$watch(function() { return query; }, function(values) {
      storage.set(STORAGE_KEY, values);
    }, true);

    /*
    query.toJSON = function() {
      return {filters: this.filters};
    };
    */

    query.param = function() {
      var param = {};

      if (angular.isDefined(query.page)) {
        param.page = query.page;
      }

      if (angular.isDefined(query.per_page)) {
        param.per_page = query.per_page;
      }

      if (angular.isDefined(query.group)) {
        param['filters[Group]'] = [query.group];
      }

      if (angular.isDefined(query.filters)) {
        angular.forEach(query.filters, function(values, filter) {
          param['filters[' + filter + ']'] = values;
        });
      }

      return param;
    };

    return query;
  }]);