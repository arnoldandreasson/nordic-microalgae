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

angular.module('nma.directives').
  directive('nmaMedia', ['metadata', function(metadata) {
    return {
      restrict: 'E',
      scope: {
        media: '=media'
      },
      link: function(scope, element) {

        var mediaFrame = element.children('.media-frame'),
            mediaFrameHeader = mediaFrame.children('.media-frame-header'),
            mediaFrameClose = mediaFrameHeader.children('.media-frame-close'),
            mediaFrameBody = mediaFrame.children('.media-frame-body'),
            mediaFrameDetails = mediaFrameBody.children('.media-frame-details'),
            mediaFrameFooter = mediaFrame.children('.media-frame-footer'),
            showDetails = mediaFrameFooter.children('.media-frame-show-details');

        function toggleDetails() {
          if (mediaFrameDetails.hasClass('media-frame-details-open')) {
            mediaFrameDetails.removeClass('media-frame-details-open');
            mediaFrameDetails.hide();
            showDetails.html('Show image information');
          } else {
            mediaFrameDetails.addClass('media-frame-details-open');
            mediaFrameDetails.show();
            showDetails.html('Hide image information');
          }
        }

        showDetails.bind('click', toggleDetails);

        function closeFrame() {
          mediaFrame.hide();
        }

        mediaFrameClose.bind('click', closeFrame);

        function openFrame() {
          mediaFrame.show();
        }

        scope.open = function(index) {
          if (angular.isNumber(index)) {
            scope.set(index);
          }
          openFrame();
        };

      },

      controller: ['$scope', function($scope) {
        var currentIndex = 0;
        $scope.hasNext = function() {
          return $scope.media && currentIndex < $scope.media.length - 1;
        };
        $scope.hasPrev = function() {
          return currentIndex > 0;
        };
        $scope.set = function(index) {
          currentIndex = index;
          $scope.currentMediaItem = $scope.media[currentIndex];
          $scope.currentMediaDescription = metadata($scope.currentMediaItem.metadata);
        };
        $scope.next = function() {
          if ($scope.hasNext()) {
            $scope.set(currentIndex + 1);
          }
        };
        $scope.prev = function() {
          if ($scope.hasPrev()) {
            $scope.set(currentIndex - 1);
          }
        };
      }],
      template:
        '<div class="mediaset clearfix">' +
          '<div class="media-item" ng-repeat="mediaItem in media">' +
            '<div class="media-item-image">' +
              '<a ng-click="open($index)">' +
                '<img ng-src="{{mediaItem.small_url}}" alt="" />' +
              '</a>' +
            '</div>' +
            '<h2 class="media-item-title">{{mediaItem.metadata.Title}}</h2>' +
          '</div>' +
        '</div>' +

        '<div class="media-frame hide">' +
          '<div class="media-frame-header">' +
            '<h2>{{currentMediaItem.metadata.Title}}</h2>' +
            '<a class="media-frame-close">Close</a>' +
          '</div>' +
          '<div class="media-frame-body">' +
            '<img class="media-frame-image" ng-src="{{currentMediaItem.large_url}}" alt="" />' +
            '<div class="media-frame-details hide">' +
              '<nma-description data="currentMediaDescription"></nma-description>' +
            '</div>' +
          '</div>' +
          '<div class="media-frame-footer">' +
            '<a class="media-frame-prev" ng-class="{disabled:!hasPrev()}" ng-click="prev()">Prev</a>' +
            '<a class="media-frame-next" ng-class="{disabled:!hasNext()}" ng-click="next()">Next</a>' +
            '<a class="media-frame-show-details">Show image information</a>' +
          '</div>' +
        '</div>'
    };
  }]);