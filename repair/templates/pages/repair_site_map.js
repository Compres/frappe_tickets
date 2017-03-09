frappe.ready(function() {
	var map = new BMap.Map("baiduMap");
	map.enableScrollWheelZoom();
	map.centerAndZoom(new BMap.Point(116.3252, 40.045103), 4);

	var opts = {
		width : 250,     // 信息窗口宽度
		height: 120,     // 信息窗口高度
		//title : "设备信息" , // 信息窗口标题
		enableMessage:true//设置允许信息窗发送短息
	};
	function addClickHandler(content,marker){
		marker.addEventListener("click",function(e){
			openInfo(content,e)}
		);
	}
	function openInfo(content,e){
		var p = e.target;
		var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
		var infoWindow = new BMap.InfoWindow(content,opts);  // 创建信息窗口对象
		map.openInfoWindow(infoWindow,point); //开启信息窗口
	}

	frappe.call({
		type: "GET",
		method: "repair.repair.doctype.repair_site.repair_site.list_site_map",
		callback: function(r) {
			if(!r.exc) {
				if(r._server_messages)
					frappe.msgprint(r._server_messages);
				else {
					var markers = [];
					var sites = r.message;
					for (var i in sites) {
						pt = new BMap.Point(sites[i].longitude, sites[i].latitude);
						var myIcon = new BMap.Icon("http://developer.baidu.com/map/jsdemo/img/fox.gif", new BMap.Size(300,157));
						var marker = new BMap.Marker(pt,{icon:myIcon});
						var content = "<a href='/iot_sites/" + sites[i].name + "'>" +
							"<h4 style='margin:0 0 5px 0;padding:0.2em 0'>" +
							sites[i].site_name + "</h4></a>" +
							"<p> Address : " + sites[i].address + "</p>" +
							"<p> Enterprise : " + sites[i].enterprise + "</p>";

						addClickHandler(content, marker);
						markers.push(marker);
					}
					//最简单的用法，生成一个marker数组，然后调用markerClusterer类即可。
					var markerClusterer = new BMapLib.MarkerClusterer(map, {markers: markers});
				}
			} else {
				if(r._server_messages)
					frappe.msgprint(r._server_messages);
				else
					frappe.msgprint(r.message);
			}
		}
	});

	frappe.call({
		type: "GET",
		method: "repair.repair.doctype.repair_site.repair_site.list_site_map",
		callback: function(r) {
			if(!r.exc) {
				if(r._server_messages)
					frappe.msgprint(r._server_messages);
				else {
					var sites = r.message;
					for (var i in sites) {
						pt = new BMap.Point(sites[i].longitude, sites[i].latitude);
						var myIcon = new BMap.Icon("http://developer.baidu.com/map/jsdemo/img/fox.gif", new BMap.Size(300, 157));
						var marker = new BMap.Marker(pt, {icon: myIcon});
						marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
						var content = "<a href='/iot_sites/" + sites[i].name + "'>" +
							"<h4 style='margin:0 0 5px 0;padding:0.2em 0'>" +
							sites[i].site_name + "</h4></a>" +
							"<p> Address : " + sites[i].address + "</p>" +
							"<p> Enterprise : " + sites[i].enterprise + "</p>";

						addClickHandler(content, marker);

						map.addOverlay(marker);
					}
				}
			} else {
				if(r._server_messages)
					frappe.msgprint(r._server_messages);
				else
					frappe.msgprint(r.message);
			}
		}
	});
});