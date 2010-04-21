/*global Ext, AJAX_FETCH, AJAX_ACTION

*/

function fgUserDialog(confOb){

var self = this;

this.frm = new fgUserForm(confOb);

if(confOb){
	this.frm.frm.getForm().setValues(confOb);
}

this.win = new Ext.Window({
	title: 'User Entry',
	iconCls: 'icoUser',
	width: 700,
	items:[ this.frm.frm ]

})

this.win.show();

} /* fgUserDialog */