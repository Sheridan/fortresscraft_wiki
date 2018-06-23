<?php

class fceBase
{

    function __construct($element_name, $where, $cache)
    {
        $this->_cache = $cache;
        $this->element_name = htmlspecialchars($element_name);
        $this->load_data($where);
        $this->namespace = '';
        switch ($where)
        {
            case 'items': $this->namespace = 'FCEItem';  break;
            case 'research': $this->namespace = 'FCEResearch';  break;
            default: $this->namespace = '';  break;
        }
    }

    protected function cache()
    {
        return $this->_cache;
    }

    protected function load_data($where)
    {
        if(!isset($this->data))
        {
            $json_file = $_SERVER["DOCUMENT_ROOT"]."/fce/json/{$where}/{$this->element_name}.json";
            $this->data = json_decode(file_get_contents($json_file), true);
        }
    }

    public function get_name()
    {
        return $this->data['name'];
    }

    public function get_page_urlpath()
    {
        return "/{$this->namespace}:{$this->element_name}";
    }

    public function get_static_icon_urlpath($dimension, $name)
    {
        return "/fce/static_icons/{$dimension}/{$name}.png";
    }

    public function get_icon_urlpath($dimension)
    {
        if($dimension != 16 && $dimension != 32 && $dimension != 64) { $dimension = 16; }

        $icon_path =  "/fce/icons/{$dimension}/{$this->element_name}.png";
        if(!file_exists($_SERVER["DOCUMENT_ROOT"].$icon_path))
        {
            $icon_path = $this->get_static_icon_urlpath($dimension, 'no_icon');
        }
        return $icon_path;
    }

    protected function get_icon_code($dimension)
    {
        if (isset($this->data['mixin']['css_icon']))
        {
            return $this->get_icon_css($dimension, $this->data['mixin']['css_icon']);
        }
        return $this->get_icon_img($dimension);
    }

    protected function get_icon_img($dimension)
    {
        return "<img class='item_icon' src='{$this->get_icon_urlpath($dimension)}' alt='{$this->get_name()}' />";
    }

    protected function get_icon_css($dimension, $id)
    {
        return "<span class='fce_icon_{$dimension}_{$id}'></span>";
    }

    protected function make_tooltip($visible_content, $tooltip_content)
    {
        return "<div class='tooltipped'>{$visible_content}<span class='tooltip_content'>{$tooltip_content}</span></div>";
    }

    protected function get_copy_to_klibboard($text, $caption)
    {
        return "<span class='copy_to_clipboard' onclick=\"copyToClibboard('{$text}')\">{$caption}</span>";
    }

    protected function get_universal_tooltip()
    {
        return "<div class='tooltip_info'>" .
                "<span class='tooltip_name'>".
                    $this->get_icon_code(16).
                    $this->get_name().
                "</span>" .
                "<span class='tooltip_copy'>Click to copy ".
                    $this->get_copy_to_klibboard($this->element_name, 'itemname').
                    $this->get_copy_to_klibboard($this->get_name(), 'name').
                    $this->get_copy_to_klibboard('https://'. $_SERVER['SERVER_NAME'] . $this->get_page_urlpath(), 'page link').
                "</span>".
                "</div>";
    }

    protected function get_tag_fce_simple($dimension, $render_text = false)
    {
        $text = '';
        if($render_text)
        {
            $text = '&nbsp;'.$this->get_name();
        }
        return $this->make_tooltip("<a href='{$this->get_page_urlpath()}'>{$this->get_icon_code($dimension)}{$text}</a>", $this->get_universal_tooltip());
    }

    protected function get_simple_key_value($key, $title, $css)
    {
        if (isset($this->data[$key]))
        {
            return "<div class='{$css}'><span class='block_caption'>{$title}</span>{$this->data[$key]}</div>";
        }
        return '';
    }

    public function get_research_requirements()
    {
        $result = '';
        if(count($this->data['research_requirement']))
        {
            $result .= "<div class='fce_participate'><span class='block_caption'>Research requirements</span>";
            foreach ($this->data['research_requirement'] as $name)
            {
                $result .= $this->cache()->get_research($name)->get_tag_fce_research(32);

            }
            $result .= "</div>";
        }
        return $result;
    }

    public function get_scan_requirements()
    {
        $result = '';
        if(count($this->data['scan_requirement']))
        {
            $result .= "<div class='fce_participate'><span class='block_caption'>Scan requirements</span>";
            foreach ($this->data['scan_requirement'] as $name)
            {
                $result .= $this->cache()->get_item($name)->get_tag_fce_item(32);
            }
            $result .= "</div>";
        }
        return $result;
    }

    public function get_properties_table($title, $what, $where = False)
    {
        if(!$where)
        {
            $where = $this->data;
        }
        $has = false;
        $result .= "<div class='fce_property_list'><span class='block_caption'>{$title}</span><table class='fce_property_table'>";
        foreach ($what as $part)
        {
            if (isset($where[$part[0]]))
            {
                $value = $where[$part[0]];
                switch($value)
                {
                    case 'true': $value = 'Yes'; break;
                    case 'false': $value = 'No'; break;
                }
                $result .= "<tr><td class='fce_property_name'>{$part[1]}</td><td class='fce_property_value'>{$value}</td></tr>";
                $has = true;
            }
        }
        $result .= "</table></div>";
        return $has ? $result : '';
    }

    public function get_items_iconlist($list_name, $caption)
    {
        $result = '';
        if(count($this->data[$list_name]))
        {
            $result .= "<div class='fce_participate'><span class='block_caption'>{$caption}</span>";
            foreach ($this->data[$list_name] as $name)
            {
                $result .=  $this->cache()->get_item($name)->get_tag_fce_item(32);
            }
            $result .= "</div>";
        }
        return $result;
    }

    public function get_researches_iconlist($list_name, $caption)
    {
        $result = '';
        if(count($this->data[$list_name]))
        {
            $result .= "<div class='fce_participate'><span class='block_caption'>{$caption}</span>";
            foreach ($this->data[$list_name] as $name)
            {
                $result .= $this->cache()->get_research($name)->get_tag_fce_research(32);
            }
            $result .= "</div>";
        }
        return $result;
    }
}
