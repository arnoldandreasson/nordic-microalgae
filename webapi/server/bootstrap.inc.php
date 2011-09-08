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

define('API_ROOT', dirname(__FILE__));
define('LIBRARY', API_ROOT . DIRECTORY_SEPARATOR . 'library');
define('INCLUDES', API_ROOT . DIRECTORY_SEPARATOR . 'includes');

require_once API_ROOT . DIRECTORY_SEPARATOR . 'config.php';
require_once INCLUDES . DIRECTORY_SEPARATOR . 'common.inc.php';

error_reporting(E_ALL|E_STRICT);
if (DEBUG === true) {
  ini_set('display_errors', 'On');
} else {
  ini_set('display_errors', 'Off');
}

$dsn = 'mysql:dbname=' . DB_NAME . ';host=' . DB_HOST;
try {
	$pdo = new PDO($dsn, DB_USER, DB_PASS);
	$pdo->exec('SET NAMES utf8');
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
  if (DEBUG === true) {
    $message = sprintf('Error: PDO %d: %s', $e->getCode(), $e->getMessage());
  } else {
    $message = 'The server encountered an unexpected condition which prevented it from fulfilling the request.';
  }
  
  header('HTTP/1.1 500 Internal Server Error');
	exit(render_json(array( 'message' => $message )));

}
unset($dsn);