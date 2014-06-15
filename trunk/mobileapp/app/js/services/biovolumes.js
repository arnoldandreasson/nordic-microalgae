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
  factory('biovolumes', ['setting', function(setting) {
    var forEach = angular.forEach,
        isDefined = angular.isDefined;

    var SETTINGS_KEY = 'HELCOM PEG';

    return function(data) {
      if (!data) {
        return;
      }

      return setting(SETTINGS_KEY).then(function(config) {
        var biovolumes = {
          sourceOfData: config['Source of data'],
          species: [],
          sizeClasses: []
        };

        biovolumes.image = config['Geometric shape images'][data['Geometric shape']];

        forEach(config['Species fields'], function(fieldName) {
          biovolumes.species.push({
            label: fieldName,
            value: data[fieldName]
          });
        });

        forEach(config['Size class fields'], function(fieldName) {
          var row = {
            label: fieldName,
            values: []
          };

          var isEmptyRow = true;

          forEach(data['Size classes'], function(sizeClass, index) {
            if (isDefined(sizeClass[fieldName])) {
              isEmptyRow = false;
              row.values[index] = sizeClass[fieldName];
            } else {
              row.values[index] = undefined;
            }
          });

          if (!isEmptyRow) {
            biovolumes.sizeClasses.push(row);
          }

        });

        return biovolumes;

      });

    };

  }]);