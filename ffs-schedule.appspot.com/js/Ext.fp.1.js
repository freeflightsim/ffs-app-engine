var AJAX_FETCH = 'app/ajax_fetch.php';
var AJAX_ACTION = 'app/ajax_action.php';

Ext.fg = function(){

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

function tick_tock_clock(){
	gToggle = !gToggle;
	gDate = gDate.add(Date.MILLI, 1000);
	var h,m,s;
	var time="        ";
	h = gDate.getHours();
	m = gDate.getMinutes();
	s = gDate.getSeconds();
	if(s<=9) s="0"+s;
	if(m<=9) m="0"+m;
	if(h<=9) h="0"+h;
	var sep =  gToggle ? ":" : " "
	sep = "<span class='real_time_blip'>" + sep + "</span>"
	time = h + sep + m + sep + s ;
	document.getElementById('real_time').innerHTML=time;
	setTimeout("tick_tock_clock()", 1000);    
}


function startInit(){
	var g = new FP_Grid();
	tick_tock_clock();
}