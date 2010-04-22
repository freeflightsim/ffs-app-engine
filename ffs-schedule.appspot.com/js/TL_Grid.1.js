

function TL_Grid(){

var self = this;


this.store = new Ext.data.JsonStore({
	url: '/rpc/timeline/',
	baseParams: {'filter': 'TODO'},
	root: 'schedule',
	idProperty: 'fppID',
	fields: [ 	'callsign', 'dep', 'arr', 'mode', 'fppID',
				'col_0','col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 
				'col_7', 'col_8', 'col_9', 'col_10', 'col_11', 'col_12', 
				'col_13', 'col_14','col_15','col_16','col_17','col_18',
				'col_19','col_20','col_21','col_22','col_23','col_24'
	],
	remoteSort: false,
	sortInfo: {field: "dep_date", direction: 'ASC'}
});


this.edit_dialog = function(fppID){
	var d = new FP_Dialog(fppID);
	d.frm.on("fpp_refresh", function(data){
		Ext.fp.msg('Saved');
		self.store.loadData(data);
	});

}
this.actionAdd = new Ext.Button({ text:'Add Entry', iconCls:'icoFppAdd', 
	handler:function(){
		self.edit_dialog(0);
	}
});
this.actionEdit = new Ext.Button({ text:'Edit', iconCls:'icoFppEdit', disabled: true,
	handler:function(){
		if( !self.selModel.hasSelection() ){
			return;
		}
		var record = self.selModel.getSelected();
		edit_dialog(record.get('fppID'));
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

this.render_airport = function(v, meta, rec){
	return rec.get('dep') + " - " + rec.get("arr");
} 
this.render_cell = function(v, meta, rec){
	
	if(!v){
		return;
	}
	var arr = v.split("|");
	if(arr[0] == 'dep'){
		meta.css = 'cell_dep'
		return arr[1];
	}else if (arr[0] == 'arr'){
		meta.css = 'cell_arr'
		return arr[1];
	}else{
		meta.css = 'cell_mid'
		return "&gt;";
	}
	
}


this.colHeaders = []
this.colHeaders.push({header: 'Callsign',  dataIndex:'callsign', sortable: true});
this.colHeaders.push({header: 'From > To',  dataIndex:'airport', sortable: true});
for(var i = 0; i < 24; i++){
	this.colHeaders.push({header: "#" + i ,  dataIndex: 'col_' + i, sortable: false});
}


//************************************************
//**  Grid
//************************************************
this.grid = new Ext.grid.GridPanel({
	iconCls: 'icoTimeline',
	title: 'Time Line',
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
	viewConfig: {emptyText: 'No item scheduled', forceFit: true}, 
	store: this.store,
	loadMask: true,
	columns: this.colHeaders,

	listeners: {},
	bbar: new Ext.PagingToolbar({
            pageSize: 50,
            store: this.store,
            displayInfo: true,
            displayMsg: 'Schedules {0} - {1} of {2}',
            emptyMsg: "No schedules to display",
            items:['-']
        })
});
this.grid.on("rowdblclick", function(grid, idx, e){
	//return;
	//self.actionEdit.execute();
	var record = self.store.getAt(idx);
	self.edit_dialog(record.get('fppID'));
	
});    
    
this.grid.on("cellclick", function(grid, rowIdx, colIdx, e){
	//console.log(rowIdx, colIdx);
	if(colIdx == 4 || colIdx == 7){
		var record = self.store.getAt(rowIdx);
		self.edit_dialog(record.get('fppID'));
	}
});   


this.load = function(){
	//self.grid.getEl().mask("Loading..");
	Ext.fp.msg('OOOPS', 'Something went wrong !');
	Ext.Ajax.request({
		url: '/rpc/timeline/',
		params: {},
		success: function(response, opts){
			//#console.log(response, opts);
			var data = Ext.decode(response.responseText);
			//console.log(data);
			if(data.error){
				alert("Error: " + data.error.description);
				return;
			}
			
			//var fpp = data.rows;
			//#for(var r in data.cols){
			//#	#console.log(r, data.cols[r]);
			//}
			colHeaders = []
			colHeaders.push({header: 'Callsign',  dataIndex:'callsign', sortable: true, renderer: self.render_callsign});
			colHeaders.push({header: 'From &gt; To',  dataIndex:'dep', sortable: true, renderer: self.render_airport});
			for(var i = 0; i < 24; i++){
				var ki = 'col_' + i;
				//console.log(ki);
				this.colHeaders.push({header: data.cols[ki],  dataIndex: ki, sortable: false, width: 30,
										align: 'center', renderer: self.render_cell});
			}
			self.grid.getColumnModel().setConfig(colHeaders);

			//var fpp = data.rows;
			for(var r=0; r < data.rows.length; r++){
				var f = data.rows[r]
				console.log(r,  f.col_ki);
				var recDef = Ext.data.Record.create([
					{name: 'fppID'},
					{name: 'callsign'},
					{name: 'dep'},
					{name: 'arr'}
				]);
				var rec = new recDef({
					fppID: f.fppID,
					callsign: f.callsign,
					dep: f.dep,
					arr: f.arr
				});
				for(var i =0; i < f.cols.length; i++){
					//console.log(i, f.cols[i]);
					var s = f.cols[i].mode + "|" + f.cols[i].time + "|" + f.cols[i].airport
					rec.set(f.cols[i].col_ki, s);
				}
				
				self.store.add(rec);
			}

			//var f = self.frm.getForm() 

			//self.frm.getEl().unmask();		
		},
		failure: function(response, opts){

			//Ext.geo.msg('OOOPS', 'Something went wrong !');
		}

	});
}
this.load();

} /***  */





