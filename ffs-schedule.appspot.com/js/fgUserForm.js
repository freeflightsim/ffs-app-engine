/*global Ext, AJAX_FETCH, AJAX_ACTION, DEV, NODE_SEP,
MyDesktop 
*/

//#############################################################################################################
//## Account Form
//#############################################################################################################

function fgUserForm(widget_div){

var self = this;
//this.Ob = confOb;

//*************************************************************************************				
//** User Form
//*************************************************************************************
this.frm = new Ext.FormPanel({
	    frame: true,
	title: 'Sign Up',
	renderTo: widget_div,
	autoHeight: true,
    url: AJAX_ACTION,
	baseParams: {fetch: 'account', },
    reader: new Ext.data.JsonReader({
				root: 'user',
				fields: [	'name', 'email','callsign', 'irc', 'cvs',
							'location', 'pass'
				]
	}),
    labelAlign: 'right',
    bodyStyle: 'padding: 20px',
    waitMsgTarget: true,
    items: [
				{xtype: 'fieldset', title: 'Details', autoHeight: true,
					items:[ {xtype: 'hidden',  name: 'action', value:'signup'},
							{fieldLabel: 'Full Name', xtype: 'textfield',  emptyText: 'eg Linus Torvalds',
								allowBlank: false, minLength: 3, name: 'name', width: '70%', msgTarget: 'side'},
							{fieldLabel: 'Email', xtype: 'textfield',  emptyText: 'Required for authenticaton', name: 'email', width: '80%', msgTarget: 'side',allowBlank: false},
							{fieldLabel: 'Password', xtype: 'textfield', allowBlank: false, minLength: 3,  name: 'pass', width: '40%', msgTarget: 'side', emptyText: 'secret',},
							{fieldLabel: 'CallSign', xtype: 'textfield',  name: 'callsign', width: '20%', msgTarget: 'side' },
							{fieldLabel: 'Irc Nick', xtype: 'textfield',  name: 'irc', width: '20%', msgTarget: 'side'},
							{fieldLabel: 'Cvs Account', xtype: 'textfield',  name: 'cvs', width: '20%', msgTarget: 'side'},
							{fieldLabel: 'Location', xtype: 'textfield',  name: 'location', width: '80%', msgTarget: 'side', emptyText: 'eg Town, Country'}
					]
				}
    ],
    buttons: [  {text: 'Submit', iconCls: 'icoClean', disabled: true,
                    handler: function(){
                        if(self.frm.getForm().isValid()){
                            self.frm.getForm().submit({
                                url: AJAX_ACTION,
                                waitMsg: 'Saving...',
                                success: function(frm, action){
									console.log(frm, action);
									var data = Ext.decode(action.response.responseText);
									console.log(data);
									if(data.error){
										alert("Error: " + data.error.description);
										return;
									}
                                    location.href= 'index.php?section=signup&page=ack';
									
                                },
                                failure: function(){

                                    //Ext.geo.msg('OOOPS', 'Something went wrong !');
                                }

                            });

                        }
                    }
                }

    ]
});



} /* fgUserForm() */