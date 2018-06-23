<?php

require_once "fceItem.php";

class fceLogo
{
    public function random()
    {
        $icons = glob($_SERVER["DOCUMENT_ROOT"]."/fce/icons/32/*.png");
        $icon = array_rand($icons);
        // echo $icon;
        $fp = fopen($icons[$icon], 'rb');

        // send the right headers
        header("Content-Type: image/png");
        header("Content-Length: " . filesize($icons[$icon]));

        // // dump the picture and stop the script
        fpassthru($fp);
        exit;
    }
}

$l = new fceLogo();
$l->random();
