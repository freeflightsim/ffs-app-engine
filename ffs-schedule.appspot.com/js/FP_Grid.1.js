

function FP_Grid(){

var self = this;




this.statusLabel = new Ext.Toolbar.TextItem({text:'Socket Status'});



//* Pilots Datastore
this.store = new Ext.data.JsonStore({
	url: '/rpc/index/',
	baseParams: {'fetch': 'schedule'},
	root: 'schedule',
	idProperty: 'fppID',
	fields: [ 	'callsign', 'fppID',
				'dep', {name: 'dep_date', type: 'date', dateFormat: 'Y-m-d H:i:s'}, 'dep_atc', 
				'arr', {name: 'arr_date', type: 'date', dateFormat: 'Y-m-d H:i:s'}, 'arr_atc',
				'comment'],
	remoteSort: false,
	sortInfo: {field: "callsign", direction: 'ASC'}
});

this.store.load();


this.actionAdd = new Ext.Button({ text:'Add Entry', iconCls:'icoFppAdd', 
				handler:function(){
					var d = new FP_Dialog();
					d.frm.on("fpp_refresh", function(){
						self.store.reload();
					});
				}
});
this.actionEdit = new Ext.Button({ text:'Edit', iconCls:'icoFppEdit', disabled: true,
				handler:function(){
					
				}
});
this.actionDelete = new Ext.Button({text:'Delete', iconCls:'icoFppDelete', disabled: true,
				handler:function(){
					  Ext.fg.msg('OOOPS', 'Something went wrong !');
				}
});




this.timmy = new Ext.Toolbar.TextItem({
	text: '12:23:45',
	width: 150
});

this.do_tick = function (){
	gToggle = !gToggle;
	gDate = gDate.add(Date.MILLI, 1000);
	var str = Ext.util.Format.date(gDate, gToggle ? "Y-m-d H:i:s" : "Y-m-d H i s" );
	self.timmy.setText(str);
}

//***************************************************************
//** Toolbar Filter Buttons / functions
//***************************************************************
this.set_filter = function(button, state){
	if(state){
		self.jobsStore.baseParams.filter = button.myFilter;
		self.jobsStore.load();
	}
    button.setIconClass( state ? 'icoFilterOn' : 'icoFilterOff');
};
this.filters = {};
this.filters.curr = new Ext.Button({
    text: 'Current',
    iconCls: 'icoFilterOn',
	enableToggle: true, allowDepress: false,
	pressed: true,
    myFilter: 'current',  toggleHandler: this.set_filter, toggleGroup: 'tbFilter'
});

this.filters.tomorrow = new Ext.Button({
    text: 'Tomorrow',
    iconCls: 'icoFilterOff',
    enableToggle: true, allowDepress: false,
    pressed: false,
    myFilter: 'completed', toggleHandler: this.set_filter, toggleGroup: 'tbFilter'
});
this.filters.after = new Ext.Button({
    text: 'After',
    iconCls: 'icoFilterOff',
    enableToggle: true, allowDepress: false,
    pressed: false,
    myFilter: 'after', toggleHandler: this.set_filter, toggleGroup: 'tbFilter'
});


//***************************************************************
//** Selection
//***************************************************************
this.selModel = new Ext.grid.RowSelectionModel({singleSelect: true});
this.selModel.on("selectionchange", function(selModel){
	self.actionEdit.setDisabled(!selModel.hasSelection())
	self.actionDelete.setDisabled(!selModel.hasSelection())
});



//***************************************************************
//** Renderers
//***************************************************************
this.render_dep = function(v, meta, rec){
	meta.css = 'fpp_dep';
	return v;
}
this.render_dep_date = function(v, meta, rec){
	meta.css = 'fpp_dep';
	return Ext.util.Format.date(v, "H:i - d M");
}
this.render_dep_atc = function(v, meta, rec){
	meta.css = 'fpp_dep';
	var c = v == "" ? 'atc_take' : 'atc_ok';
	var lbl = v == "" ? 'Take' : v;
	return "<span class='" + c + "'>" + lbl + "</span>";
}
this.render_arr = function(v, meta, rec){
	meta.css = 'fpp_arr';
	return v;
}
this.render_arr_date = function(v, meta, rec){
	meta.css = 'fpp_arr';
	return Ext.util.Format.date(v, "H:i - d M");
}
this.render_arr_atc = function(v, meta, rec){
	meta.css = 'fpp_arr';
	var c = v == "" ? 'atc_take' : 'atc_ok';
	var lbl = v == "" ? 'Take' : v;
	return "<a  class='" + c + "' href='javascript:showDialog(\"\");'>" + lbl + "</a>";
}

//************************************************
//**  Grid
//************************************************
this.grid = new Ext.grid.GridPanel({
	renderTo: 'grid_div',
	iconCls: 'icoSschedule',
	height: 600,
	deferredRender: true,
	autoScroll: true,
	enableHdMenu: false,
	layout:'fit',
	stripeRows: true,
	sm: this.selModel,
	tbar:[  this.actionAdd, '-', this.actionEdit, this.actionDelete, '-', 
			'->', '-',
			this.filters.curr, this.filters.tomorrow, this.filters.after,
			 /*   */
			'-',this.timmy
	],
	viewConfig: {emptyText: 'No servers online', forceFit: true}, 
	store: this.store,
	loadMask: true,
	columns: [  {header: '#',  dataIndex:'fppID', sortable: true, hidden: false},
				{header: 'Callsign',  dataIndex:'callsign', sortable: true},

				{header: 'Depart',  dataIndex:'dep', sortable: true, renderer: this.render_dep},
				{header: 'Date', dataIndex:'dep_date', sortable: true, renderer: this.render_dep_date},
				{header: 'ATC', dataIndex:'dep_atc', sortable: true, align: 'center',renderer: this.render_dep_atc},

				{header: 'Arrive',  dataIndex:'arr', sortable: true, renderer: this.render_arr},
				{header: 'Date', dataIndex:'arr_date', sortable: true, renderer: this.render_arr_date},
				{header: 'ATC', dataIndex:'arr_atc', sortable: true, renderer: this.render_arr_atc},

				{header: 'Comment', dataIndex:'comment', sortable: true}
	],
	listeners: {},
	bbar: new Ext.PagingToolbar({
            pageSize: 50,
            store: this.store,
            displayInfo: true,
            displayMsg: 'Servers {0} - {1} of {2}',
            emptyMsg: "No servers to display",
            items:['-']
        })
});
this.grid.on("rowdblclick", function(grid, idx, e){
	//return;
	var record = self.store.getAt(idx);
	var d = new FP_Dialog(record.get('fppID'));
});    
    
this.grid.on("cellclick", function(grid, rowIdx, colIdx, e){
	//console.log(rowIdx, colIdx);
	if(colIdx == 4 || colIdx == 7){
		var record = self.store.getAt(rowIdx);
		var d = new FP_Dialog(record.data);
	}
});   

} /***  */





