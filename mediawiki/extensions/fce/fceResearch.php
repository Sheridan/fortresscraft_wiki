<?php

require_once "fceBase.php";
require_once "fceItem.php";

class fceResearch extends fceBase
{

    function __construct($research_name, $cache)
    {
        parent::__construct($research_name, 'research', $cache);
        $this->research_name = $this->element_name;
    }


    public function get_tag_fce_research($dimension, $render_text = false)
    {
        return $this->get_tag_fce_simple($dimension, $render_text);
    }

    public function get_tag_fce_research_info()
    {
        $fcedb_name = str_replace(' ', '-', $this->research_name);
        return "<div class='item_shadowbox'>".
        "<span class='info_title'><a href='{$this->get_page_urlpath()}'>{$this->get_name()}</a></span>".
        "<div class='fce_preview_icon'>{$this->get_icon_code(64)}</div>".
        $this->get_simple_key_value('predescription', 'PreDescription', 'fce_description').
        $this->get_simple_key_value('postdescription', 'PostDescription', 'fce_description').
        "<a href='http://www.fcedb.com/research/{$fcedb_name}' target='_blank'>fcedb.com</a><br />".
        "<hr />".
                $this->get_project_requirements().
                $this->get_research_requirements().
                $this->get_scan_requirements().
                $this->get_opened_items().
                $this->get_opened_researches().
        "</div>";
    }

    public function get_project_requirements()
    {
        return $this->get_items_iconlist('participate_in_craft', "Craft with {$this->get_name()}");
    }

    private function get_opened_items()
    {
        return $this->get_items_iconlist('open_items_after_research', "Opened items");
    }

    private function get_opened_researches()
    {
        return $this->get_researches_iconlist('open_researches_after_research', "Opened researches");
    }

}
