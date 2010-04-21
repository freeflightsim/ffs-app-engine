/*global Ext, AJAX_FETCH, AJAX_ACTION

*/

function FP_Dialog(fppID){

var self = this;
console.log("fppID", fppID);
//*************************************************************************************				
//** User Form
//*************************************************************************************
this.frm = new Ext.FormPanel({
	    frame: true,
	//title: 'Sign Up',
	autoHeight: true,
    url: '/entry/edit/',
	baseParams: {fetch: 'account', },
    reader: new Ext.data.JsonReader({
				root: 'user',
				fields: [	'callsign', 
							'dep','dep_date', 'dep_time', 'dep_atc',
							'arr','arr_date', 'arr_time', 'arr_atc',
							'comments', 'email'
				]
	}),
    labelAlign: 'right',
    bodyStyle: 'padding: 20px',
    waitMsgTarget: true,
    items: [	{xtype: 'hidden',  name: 'fppID', value:'foobar'},
				/** USer **/
				{xtype: 'fieldset', title: 'Pilot', autoHeight: true, 
					items:[
						{fieldLabel: 'Callsign', xtype: 'textfield',  value: 'ac001',
								sallowBlank: false, minLength: 3, name: 'callsign', width: '30%', msgTarget: 'side'},
						{fieldLabel: 'Email', xtype: 'textfield',  value: 'foo@bar.com',
								sallowBlank: false, minLength: 3, name: 'email', width: '80%', msgTarget: 'side'}
					]
				},
				/** Departure **/
				{xtype: 'fieldset', title: 'Departure', autoHeight: true, 
					items:[
							
							{fieldLabel: 'Airport', xtype: 'textfield', minLength: 3, name: 'dep', width: '20%', msgTarget: 'side', sallowBlank: false, emptyText: 'icao', value: 'EGLL'},
							{fieldLabel: 'Date', xtype: 'datefield', sallowBlank: false, minLength: 3,   format: 'Y-m-d', 
								name: 'dep_date', width: '40%', msgTarget: 'side', boxLabel: 'If blank then today'},
							{fieldLabel: 'Time', xtype: 'timefield',  name: 'dep_time', width: '80%', msgTarget: 'side', format: 'H:i' },
							{fieldLabel: 'ATC', xtype: 'textfield',  name: 'dep_atc', width: '20%', msgTarget: 'side'}
					]
				},
				{xtype: 'fieldset', title: 'Arrival', autoHeight: true, 
					items:[
							
							{fieldLabel: 'Airport', xtype: 'textfield', minLength: 3, name: 'arr', width: '20%', msgTarget: 'side', sallowBlank: false, emptyText: 'icao', value: 'EGFF'},
							{fieldLabel: 'Date', xtype: 'datefield', sallowBlank: false, minLength: 3, format: 'Y-m-d', 
								name: 'arr_date', width: '40%', msgTarget: 'side', boxLabel: 'sssss' },
							{fieldLabel: 'Time', xtype: 'timefield',  name: 'arr_time', width: '20%', msgTarget: 'side', format: 'H:i' },
							{fieldLabel: 'ATC', xtype: 'textfield',  name: 'arr_atc', width: '20%', msgTarget: 'side'}
					]
				},
				{xtype: 'fieldset', title: 'Comment', autoHeight: true, items: [
					{hideLabel: true, xtype: 'textarea',  height: 100,
								allowBlank: true, name: 'comment', width: '95%'}
					]
				}
    ],
    buttons: [  {text: 'Submit', iconCls: 'icoClean',
                    handler: function(){
                        if(self.frm.getForm().isValid()){
                            self.frm.getForm().submit({
                                url: '/rpc/edit/',
                                waitMsg: 'Saving...',
                                success: function(frm, action){
									//console.log(frm, action);
									var data = Ext.decode(action.response.responseText);
									//console.log(data);
									if(data.error){
										alert("Error: " + data.error.description);
										return;
									}
                                    location.href= '/';
									
									
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


this.win = new Ext.Window({
	title: 'Request ATC',
	iconCls: 'icoUser',
	width: 500,
	items:[ this.frm ]

})
console.log("ere");
this.win.show();

} /* FP_Dialog */

function showFPDialog(){
	var d = new FP_Dialog();
	
	
}