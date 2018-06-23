<?php

require_once "fceCache.php";
require_once "fceItem.php";
require_once "fceResearch.php";
require_once "fceList.php";

class fce
{
    public static function onParserFirstCallInit( Parser &$parser )
    {
        $parser->setHook( 'fce_item', 'fce::renderItem' );
        $parser->setHook( 'fce_text', 'fce::renderText' );
        $parser->setHook( 'fce_info', 'fce::renderInfo' );
        $parser->setHook( 'fce_list', 'fce::renderList' );
        $parser->setHook( 'fce_research', 'fce::renderResearch' );
        $parser->setHook( 'fce_research_text', 'fce::renderResearchText' );
        $parser->setHook( 'fce_research_info', 'fce::renderResearchInfo' );
        return true;
    }

    public static function onBeforePageDisplay(OutputPage &$out, Skin &$skin)
    {
        // $out->includeJQuery();
        // $out->addScriptFile( "/extensions/fce/fce.common.js" );
        // $out->addModules( [ 'jquery' ] );
        $out->addScriptFile( "/extensions/fce/scripts/fce.common.js" );
        $out->addStyle( "/extensions/fce/styles/fce.common.css" );
        $out->addStyle( "/extensions/fce/styles/icons.css" );
        // $out->addKeyword( "fortresscraft" );
    }

    public static function renderItem( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';
        $dimension = array_key_exists('size', $args) ? intval($args['size']) : 16;

        $cache = new fceCache();
        return $cache->get_item($name)->get_tag_fce_item($dimension);
    }

    public static function renderText( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';

        $cache = new fceCache();
        return $cache->get_item($name)->get_tag_fce_item(16, true);
    }

    public static function renderInfo( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        $parser->getOutput()->addModules( 'ext.fce' );
        $parser->getOutput()->addModuleStyles( 'ext.fce.styles' );
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';

        $cache = new fceCache();
        return $cache->get_item($name)->get_tag_fce_info();

    }

    public static function renderList( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        // $parser->getOutput()->addModules( 'ext.fce' );
        // $parser->getOutput()->addModuleStyles( 'ext.fce.styles' );
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';

        $list = new fceList($name);
        return $list->get_tag_fce_list();

    }

    public static function renderResearch( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';
        $dimension = array_key_exists('size', $args) ? intval($args['size']) : 16;

        $cache = new fceCache();
        return $cache->get_research($name)->get_tag_fce_research($dimension);
    }

    public static function renderResearchText( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';

        $cache = new fceCache();
        return $cache->get_research($name)->get_tag_fce_research(16, true);
    }

    public static function renderResearchInfo( $input, array $args, Parser $parser, PPFrame $frame )
    {
        $parser->disableCache();
        $parser->getOutput()->addModules( 'ext.fce' );
        $parser->getOutput()->addModuleStyles( 'ext.fce.styles' );
        $name = array_key_exists('name', $args) ? $args['name'] : 'unknown';

        $cache = new fceCache();
        return $cache->get_research($name)->get_tag_fce_research_info();

    }
}
