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
 
class SystemSettings {
  protected $conn;
  
  function __construct(PDO $conn) {
    $this->conn = $conn;
  }
  
  function load($key) {
    $stmt = $this->conn->prepare(
      'SELECT `settings_value`
         FROM `system_settings`
        WHERE `settings_key` = :key'
    );
    $stmt->execute(array( ':key' => $key ));
    $row = $stmt->fetchObject();
    return $row ? json_decode($row->settings_value) : false;
  }
  
  function load_all() {
    $stmt = $this->conn->prepare(
      'SELECT `settings_key`, `settings_value`
         FROM `system_settings`'
    );
    $stmt->execute(array());
    
    $settings = array();
    while ($row = $stmt->fetchObject())
      $settings[$row->settings_key] = json_decode($row->settings_value);
    
    return $settings;
  }
}