/*global Ext, AJAX_FETCH, AJAX_ACTION

*/

function FP_Dialog(fppIDX){

var self = this;

this.fppID = fppIDX

this.depDate = new Ext.form.DateField({
	fieldLabel: 'Date', allowBlank: false, minLength: 3,   
	format: 'Y-m-d', 
	name: 'dep_date', width: '40%', msgTarget: 'side'
});
this.depDate.on("select", function(widget, date){
	var f = self.frm.getForm();
	var arrDate = f.findField('arr_date');
	if(arrDate.getValue() == ''){
		arrDate.setValue(widget.getValue());
	}
});

this.depTime = new Ext.form.TimeField({
	fieldLabel: 'Time', 
	name: 'dep_time', width: '80%', msgTarget: 'side', format: 'H:i' 
});
this.depTime.on("select", function(widget, date){
	var f = self.frm.getForm();
	var arrDate = f.findField('arr_time');
	if(arrDate.getValue() == ''){
		arrDate.setValue(widget.getValue());
	}
});


//console.log("fppID", fppID);
//*************************************************************************************				
//** User Form
//*************************************************************************************
this.frm = new Ext.FormPanel({
	    frame: true,
	//title: 'Sign Up',
	autoHeight: true,
    url: '/rpc/fetch/',
	baseParams: { fppID: this.fppID },
    reader: new Ext.data.JsonReader({
				root: 'fpp',
				fields: [	'callsign', 'fppID', 
							'dep','dep_date', 'dep_time', 'dep_atc',
							'arr','arr_date', 'arr_time', 'arr_atc',
							'comments', 'email'
				]
	}),
    labelAlign: 'right',
    bodyStyle: 'padding: 20px',
    waitMsgTarget: true,
    items: [	{xtype: 'hidden', name: 'fppID'},
				/*  Pilot */
				{xtype: 'fieldset', title: 'Pilot', autoHeight: true, 
					items:[
						{fieldLabel: 'Callsign', xtype: 'textfield',  
								 minLength: 3, name: 'callsign', width: '30%', msgTarget: 'side'},
						{fieldLabel: 'Email', xtype: 'textfield',   disabled: true,
								sallowBlank: false, minLength: 3, name: 'email', width: '80%', msgTarget: 'side'}
					]
				},
				/** Departure **/
				{xtype: 'fieldset', title: 'Departure', autoHeight: true, 
					items:[
							
							{fieldLabel: 'Airport', xtype: 'textfield', minLength: 3, name: 'dep', width: '20%', msgTarget: 'side', allowBlank: false, emptyText: 'icao'},
							this.depDate, this.depTime,
							{fieldLabel: 'ATC', xtype: 'textfield',  name: 'dep_atc', width: '20%', msgTarget: 'side'}
					]
				},
				/** Arrival **/
				{xtype: 'fieldset', title: 'Arrival', autoHeight: true, 
					items:[
							
							{fieldLabel: 'Airport', xtype: 'textfield', minLength: 3, name: 'arr', width: '20%', msgTarget: 'side', sallowBlank: false, emptyText: 'icao', },
							{fieldLabel: 'Date', xtype: 'datefield', sallowBlank: false, minLength: 3, format: 'Y-m-d', 
								name: 'arr_date', width: '40%', msgTarget: 'side' },
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
    buttons: [  {text: 'Submit', iconCls: 'icoSave',
                    handler: function(){
                        if(self.frm.getForm().isValid()){
                            self.frm.getForm().submit({
                                url: '/rpc/edit/',
                                waitMsg: 'Saving...',
                                success: function(frm, action){
										var data = Ext.decode(action.response.responseText);
									if(data.error){
										alert("Error: " + data.error.description);
										return;
									}
									self.frm.fireEvent("fpp_refresh", data);
                                    self.win.close();
									
									
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
	title: 'ATC Request',
	iconCls: 'icoFpp',
	width: 500,
	items:[ this.frm ]

})

this.win.show();

this.load = function(fppID){
	self.frm.getEl().mask("Loading..");
	Ext.Ajax.request({
		url: '/rpc/fetch/',
		params: {fppID: fppID},
		success: function(response, opts){
			//console.log(response, opts);
			var data = Ext.decode(response.responseText);
			//console.log(data);
			if(data.error){
				alert("Error: " + data.error.description);
				return;
			}
			
			var fpp = data.fpp;
			var f = self.frm.getForm() 
			f.findField("fppID").setValue(fpp.fppID);
			f.findField("callsign").setValue(fpp.callsign);
			f.findField("email").setValue(fpp.email);
			f.findField("comment").setValue(fpp.comment);

			f.findField("dep").setValue(fpp.dep);
			var d = Date.parseDate(fpp.dep_date, 'Y-m-d H:i:s');
			f.findField("dep_date").setValue(d);
			f.findField("dep_time").setValue(d);
			f.findField("dep_atc").setValue(fpp.dep_atc);

			f.findField("arr").setValue(fpp.arr);
			var d = Date.parseDate(fpp.arr_date, 'Y-m-d H:i:s');
			f.findField("arr_date").setValue(d);
			f.findField("arr_time").setValue(d);
			f.findField("arr_atc").setValue(fpp.arr_atc);

			f.clearInvalid();
			f.findField("arr_atc").focus();
			self.frm.getEl().unmask();		
		},
		failure: function(response, opts){

			//Ext.geo.msg('OOOPS', 'Something went wrong !');
		}

	});
}
this.load(this.fppID);



} /* FP_Dialog */


