<?php

require_once "fceBase.php";

class fceItem extends fceBase
{

    function __construct($item_name, $cache)
    {
        parent::__construct($item_name, 'items', $cache);
        $this->item_name = $this->element_name;
    }


    public function get_tag_fce_item($dimension, $render_text = false)
    {
        return $this->get_tag_fce_simple($dimension, $render_text);
    }


    public function get_tag_fce_info()
    {
        return "<div class='item_shadowbox'>".
        "<span class='info_title'><a href='{$this->get_page_urlpath()}'>{$this->get_name()}</a></span>".
        "<div class='fce_preview_icon'>{$this->get_icon_code(64)}</div>".
        $this->get_simple_key_value('description', 'Description', 'fce_description').
        "<a href='http://www.fcedb.com/{$this->item_name}' target='_blank'>fcedb.com</a><br />".
        "<hr />".
                $this->get_multiblock().
                $this->get_receipts().
                $this->get_participate_in_craft().
                $this->get_can_craft().
                $this->get_research_requirements().
                $this->get_scan_requirements().
                $this->get_open_items_after_scan().
                $this->get_open_researches_after_scan().
                $this->get_properties_table('Block properties', [
                    ['hardness', 'Hardness'],
                    ['iscolorised', 'Colorised'],
                    ['isglass', 'Glass'],
                    ['ishollow', 'Hollow'],
                    ['ispaintable', 'Paintable'],
                    ['ispassable', 'Passable'],
                    ['issolid', 'Solid'],
                    ['istransparent', 'Transparent']
                ]).
            $this->get_properties_table('Power propertyes', [
                    ['maxpowerstorage', 'Max. storage'],
                    ['powertransferpersecond', 'Transfer per second'],
                    ['powerusepersecond', 'Use per second']
                ]).
            $this->get_properties_table('Craft propertyes', [
                    ['crafttime', 'Craft time']
                ]).
            $this->get_properties_table('Fuel', [
                    ['fuel_energy', 'Gain energy']
                ]).
        "</div>";
    }

    public function get_receipts()
    {
        $result = '';
        if(count($this->data['craft_receipts']))
        {
            $result .= "<div class='fce_receipts'><span class='block_caption'>Recipts</span>";
            foreach ($this->data['craft_receipts'] as $assembler)
            {
                $result_items = array();
                foreach ($assembler['receipt'] as $name => $count)
                {
                    $ingridient_item = $this->cache()->get_item($name);
                    $result_items[] = "<div class='fce_craft_ingridient'>{$ingridient_item->get_tag_fce_item(32)}<div class='fce_ingridient_amount'>{$count}</div></div>";
                }

                $assembler_item = "<img src='{$this->get_static_icon_urlpath(32, 'hand')}' alt='Hand' />";
                if(!$assembler['cancraftanywhere'])
                {
                    $assmbl_item =  $this->cache()->get_item($assembler['assembler']);
                    $assembler_item = $assmbl_item->get_tag_fce_item(32);
                }
                $result .= "<div class='fce_craft_receipt'>".
                            "<div class='fce_craft_assembler'>{$assembler_item}</div>".
                            implode("<div class='fce_formula'>+</div>", $result_items).
                            "<div class='fce_formula'>-></div><div class='fce_craft_result'>{$this->get_tag_fce_item(32)}<div class='fce_craft_result_amount'>{$assembler['craftedamount']}</div></div>".
                            $this->get_properties_table('Recipe properties', [
                                ['researchcost', 'Research cost'],
                                ['tier', 'Tier']
                            ], $assembler).
                            "</div>";
            }
            $result .= "</div>";
        }
        return $result;
    }

    private function get_participate_in_craft()
    {
        return $this->get_items_iconlist('participate_in_craft', "Craft with {$this->get_name()}");
    }

    private function get_can_craft()
    {
        return $this->get_items_iconlist('assemble_craft', "Can craft");
    }

    private function get_multiblock()
    {
        $result = $this->get_items_iconlist('multiblock_part', "Consists of blocks");
        if(isset($this->data['part_of_multiblock_machine']))
        {
            $item =  $this->cache()->get_item($this->data['part_of_multiblock_machine']);
            $result .= "<div class='fce_participate'><span class='block_caption'>Is a part of</span>".
                       $item->get_tag_fce_item(32).
                       "</div>";
        }
        return $result;
    }

    private function get_open_items_after_scan()
    {
        return $this->get_items_iconlist('open_items_after_scan', "Open items after scan");
    }

    private function get_open_researches_after_scan()
    {
        return $this->get_researches_iconlist('open_researches_after_scan', "Open researches after scan");
    }
}
