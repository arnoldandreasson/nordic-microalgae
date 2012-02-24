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
 
class Taxa {
  
  const INCLUDE_NAVIGATION = 0x0001;
  const INCLUDE_FACTS = 0x0002;
  const INCLUDE_EXTERNAL_LINKS = 0x0004;
  const INCLUDE_MEDIA = 0x0008;
  const INCLUDE_SYNONYMS = 0x0010;
  const INCLUDE_ALL = 0xffff;
  
  protected $conn;
  
  protected $id_to_name = array();
  protected $name_to_id = array();
  
  function __construct(PDO $conn) {
    $this->conn = $conn;
  }
  
  function load($name, $attach = null) {
    $stmt = $this->conn->prepare(
      'SELECT `id`, `name`, `author`, `rank`, `parent_id`
         FROM `taxa`
        WHERE `id` = :id'
    );
    $stmt->execute(array(':id' => $this->name_to_id($name)));
    $taxon = $stmt->fetchObject();
    
    if ($taxon === false)
      return false;

    // Load and attach related data
    if (($attach & self::INCLUDE_NAVIGATION) !=0)
      $taxon->navigation = $this->navigation($taxon->name);
    
    if (($attach & self::INCLUDE_FACTS) != 0) {
      $taxon->facts = $this->facts($taxon->name);
      $taxon->external_facts = $this->external_facts($taxon->name);
      $taxon->facts_peg = $this->facts_peg($taxon->name);
    } 
    
    if (($attach & self::INCLUDE_EXTERNAL_LINKS) != 0)
      $taxon->external_links = $this->external_links($taxon->name);
    
    if (($attach & self::INCLUDE_MEDIA) != 0)
      $taxon->media = $this->media($taxon->name);
    
    if (($attach & self::INCLUDE_SYNONYMS) != 0)
      $taxon->synonyms = $this->synonyms($taxon->name);
    
    // Unset internal properties.
    unset($taxon->id, $taxon->parent_id);
    
    return $taxon;
  }
  
  function id_to_name($id) {
    if (!isset($this->id_to_name[$id])) {
      $stmt = $this->conn->prepare('SELECT `name` FROM `taxa` WHERE `id` = :id');
      $stmt->execute(array(':id' => $id));
      $this->id_to_name[$id] = $stmt->fetchColumn();
    }
    return $this->id_to_name[$id];
  }
  
  function name_to_id($name) {
    if (!isset($this->name_to_id[$name])) {
      $stmt = $this->conn->prepare('SELECT `id` FROM `taxa` WHERE `name` = :name');
      $stmt->execute(array(':name' => $name));
      $this->name_to_id[$name] = $stmt->fetchColumn();
    }
    return $this->name_to_id[$name];
  }
  
  function navigation($name) {
    $stmt = $this->conn->prepare(
      ' SELECT `prev_in_rank`, `next_in_rank`,
               `next_in_tree`, `prev_in_tree`,
               `classification`, `parent`, `children`, `siblings`
          FROM `taxa_navigation`
         WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    return $stmt->fetchObject();
  }
  
  function facts($name) {
    $stmt = $this->conn->prepare(
      'SELECT `facts_json` 
         FROM `taxa_facts`
        WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    $row = $stmt->fetchObject();
    return $row ? json_decode($row->facts_json) : false;
  }
  
  function external_facts($name) {
    $stmt = $this->conn->prepare(
      ' SELECT `provider`, `facts_json`
          FROM `taxa_external_facts`
         WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    
    $external_facts = array();
    while ($row = $stmt->fetchObject())
      $external_facts[$row->provider] = json_decode($row->facts_json);
    
    return $external_facts;
  }
  
  function facts_peg($name) {
    $stmt = $this->conn->prepare(
      ' SELECT `facts_json`
          FROM `taxa_helcom_peg`
         WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    $row = $stmt->fetchObject();
    return $row ? json_decode($row->facts_json) : false;
  }
  
  function external_links($name) {
    $stmt = $this->conn->prepare(
      ' SELECT `provider`, `type`, `value`
          FROM `taxa_external_links`
         WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    
    $external_links = array();
    while ($row = $stmt->fetchObject())
      $external_links[] = $row;
    
    return $external_links;
  }
  
  function media($name) {
    $stmt = $this->conn->prepare(
      ' SELECT `media_id`, `media_type`, `user_name`, `metadata_json` AS `metadata`
          FROM `taxa_media`
         WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    
    
    $media = array();
    while($row = $stmt->fetchObject()) {
      // Decode JSON
      $row->metadata = json_decode($row->metadata);
      
      // Set URL's for different versions
      $filename = trim(pathinfo($row->media_id, PATHINFO_FILENAME), '.');
      $row->small_url = 'http://media.nordicmicroalgae.org/small/' . $filename . '.jpg';
      //$row->medium_url = 'http://media.nordicmicroalgae.org/medium/' . $filename . '.jpg';
      $row->large_url = 'http://media.nordicmicroalgae.org/large/' . $filename . '.jpg';
      $row->original_url = 'http://media.nordicmicroalgae.org/original/' . $filename . '.jpg';
      
      $media[] = $row;
    }
    
    // Sort the media array based on media_list in taxa_media_list.
    $list_stmt = $this->conn->prepare(
      ' SELECT `media_list` 
          FROM `taxa_media_list` 
         WHERE `taxon_id` = :taxon_id'
    );
    $list_stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    $media_list = $list_stmt->fetchColumn();
    $media_list = array_flip(explode(';', $media_list));
    
    usort($media, function($a, $b) use($media_list) {
      return $media_list[$a->media_id] - $media_list[$b->media_id];
    });
   
   return $media; 
  }
  
  function synonyms($name) {
    $stmt = $this->conn->prepare(
      ' SELECT `synonym_name`, `synonym_author`, `info_json` AS `info`
          FROM `taxa_synonyms`
         WHERE `taxon_id` = :taxon_id'
    );
    $stmt->execute(array(':taxon_id' => $this->name_to_id($name)));
    
    $synonyms = array();
    while ($row = $stmt->fetchObject()) {
      $row->info = json_decode($row->info);
      $synonyms[] = $row;
    }
    return $synonyms;
  }
  
  
  function load_list(TaxaQuery $query) {
    // Set up query parts, based on choosed name status.
    switch ($query->name_status) {
      case 'accepted':
      default:
        $select = array('name', 'author', 'rank');
        $from   = array('taxa');
        $where  = array();
        $order  = array('name ASC');
        break;
        
      case 'synonym':
        $select = array('synonym_name', 'synonym_author', 'name', 'author', 'rank');
        $from   = array('taxa_synonyms, taxa');
        $where  = array('taxa_synonyms.taxon_id = taxa.id');
        $order  = array('synonym_name ASC');
        break;
    }
    
    $params = array();

    // Add WHERE name/synonym_name LIKE clause and parameters.
    if (!empty($query->name)) {
      // Use different fields depending on name status.
      switch ($query->name_status) {
        case 'accepted':
        default:
          $name_field = 'taxa.name';
          break;
          
        case 'synonym':
          $name_field = 'taxa_synonyms.synonym_name';
          break;
      }
      
      $name_where = array();
      for ($i = 0; $i < count($query->name); $i++) {
        $param_name = sprintf(':name_%u', $i);
        $name_where[] = "$name_field LIKE $param_name";

        // Replace custom wildcard characters with MySQL wildcard characters, if specified.
        if (strpos($query->name[$i], '*') !== false)
          $params[$param_name] = str_replace('*', '%', $query->name[$i]);
        else
          $params[$param_name] = "{$query->name[$i]}%";        
      }
      $where[] = '(' . implode(' OR ', $name_where) . ')';
    }


    // Add WHERE taxa.rank clause and parameters.
    if (!empty($query->rank)) {
      $rank_where = array();
      for ($i = 0; $i < count($query->rank); $i++) {
        $param_name = sprintf(':rank_%u', $i);
        $rank_where[] = "taxa.rank = $param_name";

        $params[$param_name] = $query->rank[$i];
      }
      $where[] = '(' . implode(' OR ', $rank_where) . ')';
    }


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

        $filter_query = 'SELECT taxon_id FROM taxa_filter_search WHERE ' . implode('OR', $filter_where);
        $where[] = "(taxa.id IN ($filter_query))";
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


    // Execute the query and return results.
    $stmt = $this->conn->prepare($sql);

    foreach ($params as $param => $value) {
      if ($param == ':offset' || $param == ':limit')
        $stmt->bindValue($param, $value, PDO::PARAM_INT);
      else
        $stmt->bindValue($param, $value);
    }

    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
  }
  
}