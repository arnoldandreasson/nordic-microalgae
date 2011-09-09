<?php
/**
 * Nordic Microalgae. http://nordicmicroalgae.org/
 *
 * @author Andreas Loo, info@andreasloo.se
 * @copyright (c) 2011 SMHI, Swedish Meteorological and Hydrological Institute
 * @license: MIT License as follows:
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
 
function render_json($data) {
  $output = json_encode($data);
  
  if (!empty($_GET['callback'])) {
    header('Content-Type: application/javascript; charset=utf-8');
    $output = ((string) $_GET['callback']) . '(' . $output . ')';
  } else {
    header('Content-Type: application/json; charset=utf-8');
  }
 
 print $output;
}