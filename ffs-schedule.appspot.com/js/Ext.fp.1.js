var AJAX_FETCH = 'app/ajax_fetch.php';
var AJAX_ACTION = 'app/ajax_action.php';

Ext.fp = function(){

   var msgCt;
    function createBox(t, s){
        return ['<div class="msg">',
                '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
                '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc"><h3>', t, '</h3>', s, '</div></div></div>',
                '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
                '</div>'].join('');
    }

    return {
        msg : function(title, body, tim){
            if(!msgCt){
                msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
            }
            msgCt.alignTo(document, 't-t');
            //var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
            var m = Ext.DomHelper.append(msgCt, {html:createBox(title, body)}, true);
            var Timmy = tim > 0 ? tim : 3;
            m.slideIn('t').pause(Timmy).ghost("t", {remove:true});
        },

        init : function(){
        }

	};

}();

var widget;

function tick_tock_clock(){
	gToggle = !gToggle;
	gDate = gDate.add(Date.MILLI, 1000);
	document.getElementById('real_date').innerHTML = Ext.util.Format.date(gDate, "d F Y" ); 
	document.getElementById('real_time').innerHTML = Ext.util.Format.date(gDate, gToggle ? "H:i:s" : "H.i.s" ); 
	setTimeout("tick_tock_clock()", 1000); 
}

function startInit(){
	var pilotRequestsGrid = new FP_Grid();
	var timelineGrid = new TL_Grid();


	var tabWidget = new Ext.TabPanel({
	activeTab: 0,
	renderTo: 'grid_div',
	plain: true,
	height: 600,
	items:[
		timelineGrid.grid
		, pilotRequestsGrid.grid
	]
	});

	
	tick_tock_clock();
}