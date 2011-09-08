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
 
class TaxaQuery {
  protected $_name = array();
  protected $_rank = array();
  protected $_filters = array();
  
  protected $_page;
  protected $_pages;
  protected $_per_page;
  protected $_total;
  
  function set_name(array $name = array()) {
    $this->_name = $name;
  }
  
  function set_rank(array $rank = array()) {
    $this->_rank = $rank;
  }
  
  function set_filters(array $filters = array()) {
    $this->_filters = $filters;
  }
  
  function set_page($page) {
    $this->_page = (int) $page;
  }
  
  function set_per_page($per_page) {
    $this->_per_page = (int) $per_page;
  }
  
  function set_pages($pages) {
    $this->_pages = (int) $pages;
  }
  
  function set_total($total) {
    $this->_total = (int) $total;
  }
  
  function __isset($var) {
    return isset($this->{"_$var"});
  }
  
  function __get($var) {
    $method = sprintf('get_%s', strtolower($var));
    if (is_callable(array($this, $method)))
      return call_user_func(array($this, $method));
    
    return $this->{"_$var"};    
  }
  
  function __set($var, $value) {
    $method = sprintf('set_%s', strtolower($var));
    if (is_callable(array($this, $method)))
      return call_user_func_array(array($this, $method), array($value));

    return $this->{"_$var"} = $value;    
  }
}
