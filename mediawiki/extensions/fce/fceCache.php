<?php

require_once "fceItem.php";
require_once "fceResearch.php";
require_once "fceList.php";

class fceCache
{
    function __construct()
    {
        $this->cache = ['FCEItem' => [], 'FCEResearch' => []];
    }

    public function get_element($space, $index_name)
    {
        if(!isset($this->cache[$space][$index_name]))
        {
            $element = null;
            switch ($space)
            {
                case 'FCEItem'    :
                case 'items'       : $element = new fceItem    ($index_name, $this); break;
                case 'FCEResearch':
                case 'research'   : $element = new fceResearch($index_name, $this); break;
            }
            $this->cache[$space][$index_name] = $element;
        }
        return $this->cache[$space][$index_name];
    }

    public function get_item($index_name)
    {
        return $this->get_element('FCEItem', $index_name);
    }

    public function get_research($index_name)
    {
        return $this->get_element('FCEResearch', $index_name);
    }
}
