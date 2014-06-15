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
  factory('Filter', ['setting', 'storage', function(setting, storage) {
    var SETTING_KEY = 'Filters',
        STORAGE_KEY = 'filter-states';

    var forEach = angular.forEach;

    var promise = setting(SETTING_KEY).then(function(config) {
      // Don't modify the original object
      var filters = angular.copy(config);

      // Mark selected
      var states = storage.get(STORAGE_KEY);
      forEach(filters.Groups, function(group) {
        forEach(group, function(filter) {
          if (filter.Filter in states && filter.Value in states[filter.Filter]) {
            filter.Selected = states[filter.Filter][filter.Value];
          } else {
            filter.Selected = filter.Default === 'True';
          }
        });
      });

      return filters;
    });

    return {
      get: function() {
        return promise;
      },
      reset: function() {
        promise.then(function(config) {
          forEach(config.Groups, function(filters) {
            forEach(filters, function(filter) {
              filter.Selected = filter.Default === 'True';
            });
          });
        });
      },
      save: function() {
        return promise.then(function(config) {
          var states = {};
          forEach(config.Groups, function(filters) {
            forEach(filters, function(filter) {
              states[filter.Filter] = states[filter.Filter] || {};
              states[filter.Filter][filter.Value] = filter.Selected ? true : false;
            });
          });
          storage.set(STORAGE_KEY, states);

          return config;
        });
      }
    };

  }]);