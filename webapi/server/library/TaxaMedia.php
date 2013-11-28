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

class TaxaMedia {
  protected $conn;
  
  function __construct(PDO $conn) {
    $this->conn = $conn;
  }

  function load($media_id) {
    $stmt = $this->conn->prepare(
      ' SELECT `media_id`, `media_type`, `user_name`, `metadata_json`
          FROM `taxa_media`
         WHERE `media_id` = :media_id'
    );
    $stmt->execute(array(':media_id' => $media_id));
    $row = $stmt->fetchObject();

    if ($row === false)
      return false;

    $this->setup_row($row);
    return $row;
  }

  function load_list(TaxaMediaQuery $query) {
    $select = array('media_id', 'media_type', 'user_name', 'metadata_json');
    $from   = array('taxa_media');
    $where  = array();
    $order  = array('media_id ASC');

    $params = array();

    // Add filter clauses and parameters.
    if (!empty($query->filters)) {
      $filter_num = 0;

      foreach ($query->filters as $filter => $filter_values) {
        $filter_where = array();

        foreach ((array) $filter_values as $filter_value) {
          $param_filter_name = sprintf(':filter_%u', $filter_num);
          $param_filter_value_name = sprintf(':filter_value_%u', $filter_num);

          $filter_where[] = "(filter = $param_filter_name AND value = $param_filter_value_name)";

          $params[$param_filter_name] = $filter;
          $params[$param_filter_value_name] = $filter_value;

          $filter_num++;
        }

        $filter_query = 'SELECT media_id FROM taxa_media_filter_search WHERE ' . implode(' OR ', $filter_where);
        $where[] = "(taxa_media.media_id IN ($filter_query))";
      }
    }

    // Construct SQL out of the query parts.
    $select = empty($select) ? '' : '   SELECT ' . implode(', ', $select);
    $from   = empty($from)   ? '' : '     FROM ' . implode(', ', $from);
    $where  = empty($where)  ? '' : '    WHERE ' . implode( ' AND ', $where);
    $order  = empty($order)  ? '' : ' ORDER BY ' . implode(', ', $order);

    $sql = $select . $from . $where . $order;

    // Count records and update paging properties if the per_page parameter is set.
    if (isset($query->per_page)) {
      $stmt = $this->conn->prepare('SELECT count(*) AS total' . $from . $where);
      $stmt->execute($params);
      $count = $stmt->fetchObject();
      unset($stmt);

      if (empty($query->page))
        $query->page = 1;

      // Calculate and update paging properties.
      $query->total = $count->total;
      if ($query->total <= $query->per_page) {
        $query->page = $query->pages = 1;
      } else {
        $query->pages = ceil($query->total / $query->per_page);
        if ($query->page > $query->pages)
          $query->page = $query->pages;
      }

      // Add limit clause and parameters.
      $sql .= ' LIMIT :offset, :limit';
      $params[':offset'] = (($query->page - 1) * $query->per_page);
      $params[':limit'] = $query->per_page;
    }

    // Execute query.
    $stmt = $this->conn->prepare($sql);

    foreach ($params as $param => $value) {
      if ($param == ':offset' || $param == ':limit')
        $stmt->bindValue($param, $value, PDO::PARAM_INT);
      else
        $stmt->bindValue($param, $value);
    }

    $stmt->execute();

    $media = array();
    while ($row = $stmt->fetchObject()) {
      $this->setup_row($row);
      $media[] = $row;
    }

    return $media;
  }

  function setup_row($row) {
    // Decode JSON
    $row->metadata = json_decode($row->metadata_json);
    unset($row->metadata_json);

    // Set URL's for different versions
    $filename = trim(pathinfo($row->media_id, PATHINFO_FILENAME), '.');
    $row->small_url = 'http://media.nordicmicroalgae.org/small/' . $filename . '.jpg';
    //$row->medium_url = 'http://media.nordicmicroalgae.org/medium/' . $filename . '.jpg';
    $row->large_url = 'http://media.nordicmicroalgae.org/large/' . $filename . '.jpg';
    $row->original_url = 'http://media.nordicmicroalgae.org/original/' . $filename . '.jpg';
  }

  function create($media) {
    
  }
  
  function update($media) {
    
  }
  
}