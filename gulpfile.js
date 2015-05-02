/**
 * Gulpfile.js - RocketPod
 */


'use strict';


/**
 * Dependencies
 */

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();


/**
 * Constants
 */

var AUTOPREFIXER_BROWSERS = [
  'chrome >= 30',
  'ie >= 8',
  'ff >= 24',
  'safari >= 6',
  'opera >= 12',
  'ios >= 6',
  'android 2.3',
  'android >= 4',
  'ie_mob >= 9'
];

/**
 * Compile and compress SCSS and JS files
 */

// CSS
gulp.task('static:css', function () {
  return gulp.src('src/scss/main.scss')
    .pipe($.sass({
      outputStyle: 'compressed',
      loadPath: ['src/scss']
    }))
    .on('error', function (e) { console.error(e.message); })
    .pipe($.autoprefixer(AUTOPREFIXER_BROWSERS))
    .pipe(gulp.dest('static/css'));
});

// JS
gulp.task('static:js', function () {
  return gulp.src('src/js/*.js')
    .pipe($.concat('main.js'))
    .pipe($.uglify())
    .pipe(gulp.dest('static/js'));
});

// Images
gulp.task('static:images', function () {
  return gulp.src('src/images/*')
    .pipe(gulp.dest('static/images'));
});

// Vendor JS - Add files manually
gulp.task('vendor:js', function () {
  return gulp.src([
      'bower_components/jquery/dist/jquery.min.js'
  ])
    .pipe($.concat('vendor.js'))
    .pipe($.uglify())
    .pipe(gulp.dest('static/js'));
});

// Vendor CSS - Add files manually
gulp.task('vendor:css', function () {
  return gulp.src([
      'bower_components/fontawesome/css/font-awesome.min.css'
  ])
    .pipe($.concat('vendor.css'))
    .pipe(gulp.dest('static/css'));
});

// Vendor fonts - Add files manually
gulp.task('vendor:fonts', function () {
  return gulp.src([
      'bower_components/fontawesome/fonts/*'
  ])
    .pipe(gulp.dest('static/fonts'));
});

gulp.task('static', [
    'static:css',
    'static:js',
    'static:images',
    'vendor:css',
    'vendor:js',
    'vendor:fonts'
]);

/**
 * Watch for changes
 */

gulp.task('watch', ['static'], function () {
  gulp.watch('src/scss/**/*.scss', ['static:css']);
  gulp.watch('src/js/**/*.js', ['static:js']);
});

/**
 * Default
 */

gulp.task('default', ['static']);
