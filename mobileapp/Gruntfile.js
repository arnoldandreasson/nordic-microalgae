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

/*global module*/
'use strict';

module.exports = function(grunt) {
  grunt.initConfig({
    banner: [
      '/*',
      ' Nordic Microalgae Mobile. http://m.nordicmicroalgae.org',
      '',
      ' Author: Andreas Loo, info@andreasloo.se',
      ' Copyright (c) 2013 SMHI, Swedish Meteorological and Hydrological Institute',
      ' License: MIT License as follows:',
      '',
      ' Permission is hereby granted, free of charge, to any person obtaining a copy',
      ' of this software and associated documentation files (the "Software"), to deal',
      ' in the Software without restriction, including without limitation the rights',
      ' to use, copy, modify, merge, publish, distribute, sublicense, and/or sell',
      ' copies of the Software, and to permit persons to whom the Software is',
      ' furnished to do so, subject to the following conditions:',
      '',
      ' The above copyright notice and this permission notice shall be included in',
      ' all copies or substantial portions of the Software.',
      '',
      ' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR',
      ' IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,',
      ' FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE',
      ' AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER',
      ' LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,',
      ' OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN',
      ' THE SOFTWARE.',
      '*/'
    ].join('\n'),

    connect: {
      server: {
        options: {
          port: 8000,
          hostname: 'localhost',
          base: 'app',
          keepalive: true
        }
      }
    },

    clean: {
      dist: ['dist']
    },

    concat: {
      js: {
        files: [
          {
            dest: 'dist/js/lib-<%= grunt.template.today("yyyymmdd") %>.js',
            src: [
              'app/lib/jquery.min.js',
              'app/lib/bootstrap/js/bootstrap.min.js',
              'app/lib/angular/angular.min.js',
              'app/lib/angular/angular-resource.min.js',
              'app/lib/angular/angular-sanitize.min.js'
            ]
          },
          {
            dest: 'dist/js/app-<%= grunt.template.today("yyyymmdd") %>.js',
            src: [
              'app/js/app.js',
              'app/js/**/*.js'
            ]
          }
        ]
      },
      css: {
        files: [
          {
            dest: 'dist/css/lib-<%= grunt.template.today("yyyymmdd") %>.css',
            src: [
              'app/lib/bootstrap/css/bootstrap.min.css',
              'app/lib/bootstrap/css/bootstrap-responsive.min.css'
            ]
          },
          {
            dest: 'dist/css/app-<%= grunt.template.today("yyyymmdd") %>.css',
            src: [
              'app/css/app.css',
              'app/css/**/*.css'
            ]
          }
        ]
      }
    },

    copy: {
      dist: {
        files: [
          {
            expand: true,
            cwd: 'app',
            src: [
              '*.{html,ico,txt,webapp}',
              '.htaccess',
              'img/**/*',
              'views/**/*'
            ],
            dest: 'dist'
          }
        ]
      }
    },

    cssmin: {
      dist: {
        files: [
          {
            src: 'dist/css/app-<%= grunt.template.today("yyyymmdd") %>.css',
            dest: 'dist/css/app-<%= grunt.template.today("yyyymmdd") %>.css'
          }
        ],
        options: {
          banner: '<%= banner %>'
        }
      }
    },

    uglify: {
      dist: {
        files: [
          {
            src: 'dist/js/app-<%= grunt.template.today("yyyymmdd") %>.js',
            dest: 'dist/js/app-<%= grunt.template.today("yyyymmdd") %>.js'
          }
        ],
        options: {
          banner: '<%= banner %>\n'
        }
      }
    },

    jshint: {
      all: ['Gruntfile.js', 'app/js/**/*.js'],
      options: {
        jshintrc: '.jshintrc'
      }
    }

  });

  // Alias tasks
  grunt.registerTask('server', ['connect:server']);
  grunt.registerTask('build', ['clean', 'copy', 'concat', 'cssmin', 'uglify', 'updatehtml']);
  grunt.registerTask('default', ['jshint', 'build']);

  // Custom tasks
  grunt.registerTask('updatehtml', 'Update HTML to include concatenated scripts and styles.', function() {
    var contents = grunt.file.read('dist/index.html');

    // Replace scripts
    contents = contents.replace(/<!-- scripts -->([\s\S]*?)<!-- \/scripts -->/,
      grunt.config('concat.js.files').map(function(file) {
        return '<script src="' + file.dest.replace(/^dist\//, '') + '"></script>';
      }).join('\n  ')
    );

    // Replace styles
    contents = contents.replace(/<!-- styles -->([\s\S]*?)<!-- \/styles -->/,
      grunt.config('concat.css.files').map(function(file) {
        return '<link rel="stylesheet" href="' + file.dest.replace(/^dist\//, '') + '" />';
      }).join('\n  ')
    );

    grunt.file.write('dist/index.html', contents);
  });

  // Load plugins
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-connect');
};