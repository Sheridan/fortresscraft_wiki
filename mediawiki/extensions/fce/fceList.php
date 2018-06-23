<?php

require_once "fceItem.php";

class fceList
{
    function __construct($list_name)
    {
        $this->list_name = htmlspecialchars($list_name);
        $this->load_data();
    }

    private function load_data()
    {
        if(!isset($this->list_data))
        {
            $json_file = $_SERVER["DOCUMENT_ROOT"]."/fce/json/lists/{$this->list_name}.json";
            $this->list_data = json_decode(file_get_contents($json_file), true);
        }
    }

    public function get_tag_fce_list()
    {
        $result .= "<div class='fce_items_list'>";
        foreach ($this->list_data as $name)
        {
            $cache = new fceCache();
            $result .= $cache->get_item($name)->get_tag_fce_item(32);
        }
        $result .= "</div>";
        return $result;
    }
}
