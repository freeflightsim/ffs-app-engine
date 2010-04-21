

function fgServersGrid(){

var self = this;



this.statusLabel = new Ext.Toolbar.TextItem({text:'Socket Status'});



//* Pilots Datastore
this.store = new Ext.data.JsonStore({
	url: AJAX_FETCH,
	baseParams: {'fetch': 'servers'},
	root: 'servers',
	idProperty: 'server_id',
	fields: [ 	'server_id', 'server_type_id', 'server_type', 'host', 'nick', 'type', 'ip' ,'location','comment','contact','irc', 'tracked','active'],
	remoteSort: false,
	sortInfo: {field: "host", direction: 'ASC'}
});

this.store.load();


this.actionAdd = new Ext.Button({ text:'Add', iconCls:'icoServerAdd', 
				handler:function(){
					var d = new fgServerDialog();
				}
});
this.actionEdit = new Ext.Button({ text:'Edit', iconCls:'icoServerEdit', disabled: true,
				handler:function(){
					
				}
});
this.actionDelete = new Ext.Button({text:'Delete', iconCls:'icoServerDelete', disabled: true,
				handler:function(){
					  Ext.fg.msg('OOOPS', 'Something went wrong !');
				}
});

this.selModel = new Ext.grid.RowSelectionModel({singleSelect: true});
this.selModel.on("selectionchange", function(selModel){
	self.actionEdit.setDisabled(!selModel.hasSelection())
	self.actionDelete.setDisabled(!selModel.hasSelection())
});

//************************************************
//** Servers  Grid
//************************************************
this.grid = new Ext.grid.GridPanel({
	title: 'Servers Administration',
	renderTo: 'widget_div',
	iconCls: 'icoServers',
	height: 500,
	deferredRender: true,
	autoScroll: true,
	enableHdMenu: false,
	layout:'fit',
	sm: this.selModel,
	tbar:[ 	this.actionAdd, this.actionEdit, this.actionDelete
	],
	viewConfig: {emptyText: 'No servers online', forceFit: true}, 
	store: this.store,
	loadMask: true,
	columns: [  {header: '#',  dataIndex:'server_id', sortable: true, hidden: true},
				{header: 'Nick',  dataIndex:'nick', sortable: true},
				{header: 'Type',  dataIndex:'server_type', sortable: true},
				{header: 'Host', dataIndex:'host', sortable: true},
				{header: 'Ip', dataIndex:'ip', sortable: true, align: 'center'},
				{header: 'Location', dataIndex:'location', sortable: true, align: 'left'},
				{header: 'Contact', dataIndex:'contact', sortable: true, align: 'left',
					renderer: function(v, meta, rec){
						var s = ''
						if(rec.get('irc')){
							s += "#" + rec.get('irc') + " - ";
						}
						if(rec.get('contact')){
							s += rec.get('contact') 
						}
						return s;
					}
				},
				{header: 'Trk', dataIndex:'tracked', sortable: true, align: 'center', width: 40},
				{header: 'Active', dataIndex:'active', sortable: true, align: 'center', width: 40}
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
	var record = self.store.getAt(idx);
	var d = new fgServerDialog(record.data);
});    
    



} /***  */





