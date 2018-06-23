var addGroup = function (name)
{
  data = {
    'section': 'advanced',
    'groups': {}
  };
  data['groups'][name+'_group'] = { 'label': name };
  $( '#wpTextbox1' ).wikiEditor( 'addToToolbar', data );
};

var simpleAddButton = function(group, label, icon, pre, peri, post)
{
  $('#wpTextbox1').wikiEditor('addToToolbar', {
    'section': 'advanced',
    'group': group+'_group',
    'tools': {
      'buttonId': {
        'label': label,
        'type': 'button',
        'icon': icon,
        'action': {
          'type': 'encapsulate',
          'options': {
            'pre': pre,
            'peri': peri,
            'post': post
          }
        }
      }
    }
  });
};

var addFCEButton = function(label, icon, pre, peri, post)
{
  simpleAddButton('FCE', label, '/fce/icons/16/'+icon+'.png', pre, peri, post);
};

var addUsefulButton = function(label, icon, pre, peri, post)
{
  simpleAddButton('Useful', label, '/fce/static_icons/16/'+icon+'.png', pre, peri, post);
};

var customizeFCE = function()
{
  addGroup('FCE');

  addFCEButton('Insert FCE Item icon tag', 'manufacturingplant', "<fce_item name='", "item_name", "' />");
  addFCEButton('Insert FCE Item text tag', 'slodrs', "<fce_text name='", "item_name", "' />");
  addFCEButton('Insert FCE Research icon tag', 'laboratory', "<fce_research name='", "research_name", "' />");
  addFCEButton('Insert FCE Research text tag', 'orbitalpower', "<fce_research_text name='", "research_name", "' />");

  addFCEButton('Insert FCE Item info tag (For using in item pages)', 'cryomap', "<fce_info name='", "item_name", "' />");
  addFCEButton('Insert FCE Research info tag (For using in research pages)', 't4defence1a', "<fce_research_info name='", "research_name", "' />");

  addGroup('Useful');
  addUsefulButton('Keyboard shortcut', 'kb_shortcut', "{{shortcut|", "shortcut", "}}");
};

var customizeToolbar = function ()
{
  customizeFCE();
};

(window.RLQ=window.RLQ||[]).push(function(){
/* Check if view is in edit mode and that the required modules are available. Then, customize the toolbar … */
if ( $.inArray( mw.config.get( 'wgAction' ), [ 'edit', 'submit' ] ) !== -1 ) {
	mw.loader.using( 'user.options' ).then( function () {
		// This can be the string "0" if the user disabled the preference ([[phab:T54542#555387]])
		if ( mw.user.options.get( 'usebetatoolbar' ) == 1 ) {
			$.when(
				mw.loader.using( 'ext.wikiEditor' ), $.ready
			).then( customizeToolbar );
		}
	} );
}
});

var copyToClibboard = function(text)
{
  const el = document.createElement('textarea');  // Create a <textarea> element
  el.value = text;                               // Set its value to the string that you want copied
  el.setAttribute('readonly', '');                // Make it readonly to be tamper-proof
  el.style.position = 'absolute';
  el.style.left = '-9999px';                      // Move outside the screen to make it invisible
  document.body.appendChild(el);                  // Append the <textarea> element to the HTML document
  const selected =
    document.getSelection().rangeCount > 0        // Check if there is any content selected previously
      ? document.getSelection().getRangeAt(0)     // Store selection if found
      : false;                                    // Mark as false to know no selection existed before
  el.select();                                    // Select the <textarea> content
  document.execCommand('copy');                   // Copy - only works as a result of a user action (e.g. click events)
  document.body.removeChild(el);                  // Remove the <textarea> element
  if (selected)                                   // If a selection existed before copying
  {
    document.getSelection().removeAllRanges();    // Unselect everything on the HTML document
    document.getSelection().addRange(selected);   // Restore the original selection
  }
}


