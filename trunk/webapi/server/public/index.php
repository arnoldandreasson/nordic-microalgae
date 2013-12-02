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

require_once dirname(dirname(__FILE__)) . DIRECTORY_SEPARATOR . 'bootstrap.inc.php';
require_once LIBRARY . DIRECTORY_SEPARATOR . 'Taxa.php';
require_once LIBRARY . DIRECTORY_SEPARATOR . 'TaxaQuery.php';
require_once LIBRARY . DIRECTORY_SEPARATOR . 'TaxaMedia.php';
require_once LIBRARY . DIRECTORY_SEPARATOR . 'TaxaMediaQuery.php';
require_once LIBRARY . DIRECTORY_SEPARATOR . 'SystemSettings.php';

$cmd = !empty($_GET['cmd']) ? $_GET['cmd'] : null;
switch ($cmd) {
  
  // Load and return taxon and related data.
  // URL: taxa/Dinophysis acuta.json or taxa/Dinophysis acuta/$part.json
  case 'taxon':
    $taxa = new Taxa($pdo);

    $name = !empty($_GET['name']) ? $_GET['name'] : null;
    $part = !empty($_GET['part']) ? $_GET['part'] : null;

    // Slashes in taxon names are replaced by underscores in URLs.
    $name = str_replace('_', '/', $name);

    // Load taxon and all or a specific part of related data.
    $taxon = false;
    if ($part === null) {
      $taxon = $taxa->load($name, Taxa::INCLUDE_ALL);
    } elseif (defined('Taxa::INCLUDE_' . strtoupper($part))) {
      $taxon = $taxa->load($name, constant('Taxa::INCLUDE_' . strtoupper($part)));
    }

    if ($taxon === false) {
      header('HTTP/1.1 404 Not Found');
      exit(render_json(array('message' => 'Not Found')));
    }

    if ($part === null) {
      $response = $taxon;
    } elseif ($part === 'facts') {
      $response = array(
        'facts'           => $taxon->facts,
        'external_facts'  => $taxon->external_facts,
        'facts_peg'       => $taxon->facts_peg,
      );
    } else {
      $property = strtolower($part);
      $response = array($property => $taxon->$property);
    }
    
    render_json($response);
    break;

  // Load and return a list of taxa.
  // URL: taxa.json
  case 'taxon-list':
    $taxa = new Taxa($pdo);
    $query = new TaxaQuery();
    
    if (!empty($_GET['name_status']))
      $query->name_status = $_GET['name_status'];
    
    if (!empty($_GET['name']))
      $query->name = (array) $_GET['name'];
    
    if (!empty($_GET['rank']))
      $query->rank = (array) $_GET['rank'];
    
    if (!empty($_GET['filters']))
      $query->filters = (array) $_GET['filters'];

    if (!empty($_GET['page']))
      $query->page = $_GET['page'];

    if (!empty($_GET['per_page']))
      $query->per_page = $_GET['per_page'];

    $taxa = $taxa->load_list($query);    
    if (isset($query->per_page)) {
      $total = $query->total;
      $page = $query->page;
      $pages = $query->pages;
      $per_page = $query->per_page;
    }
    
    $response = compact('taxa', 'total', 'page', 'pages', 'per_page');
    render_json($response);
    break;

  // Load and return a list of artists/photographers.
  // URL: media/artists.json
  case 'artist-list':
    $media = new TaxaMedia($pdo);
    $response = array('artists' => $media->load_artist_list());
    render_json($response);
    break;

  // Load and return media item.
  // URL: media/Dinophysis acuta_1.gif.json
  case 'media':
    $media = new TaxaMedia($pdo);

    $response = false;
    if (!empty($_GET['media_id'])) {
      $response = $media->load($_GET['media_id']);
    }

    if ($response === false) {
      header('HTTP/1.1 404 Not Found');
      exit(render_json(array('message' => 'Not Found')));
    }

    render_json($response);
    break;

  // Load and return a list of media items.
  // URL: media.json
  case 'media-list':
    $media = new TaxaMedia($pdo);
    $query = new TaxaMediaQuery();

    if (!empty($_GET['filters']))
      $query->filters = (array) $_GET['filters'];

    if (!empty($_GET['page']))
      $query->page = $_GET['page'];

    if (!empty($_GET['per_page']))
      $query->per_page = $_GET['per_page'];

    $media = $media->load_list($query);
    if (isset($query->per_page)) {
      $total = $query->total;
      $page = $query->page;
      $pages = $query->pages;
      $per_page = $query->per_page;
    }

    $response = compact('media', 'total', 'page', 'pages', 'per_page');
    render_json($response);
    break;

  // Load and return one or all setting(s).
  // URL: settings.json or settings/$settings_key.json
  case 'setting':
    $settings = new SystemSettings($pdo);
    
    if (!empty($_GET['key'])) {
      $response = $settings->load($_GET['key']);
    } else {
      $response = $settings->load_all();
    }

    if ($response === false) {
      header('HTTP/1.1 404 Not Found');
      exit(render_json(array('message' => 'Not Found')));
    }
    
    render_json($response);
    break;
  
  
  // Return 404 Not Found for unknown commands.
  default:
    header('HTTP/1.1 404 Not Found');
    exit(render_json(array('message' => 'Not Found')));
  
}