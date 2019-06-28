function JsonToUrl(jsn, ip) {
	var obj = JSON.parse(jsn);
	var url = [];
	for (var i in obj) {
		url.push(ip + 'task/' + obj[i]);
	}
	return url;
}
module.exports = {
	JsonToUrl: JsonToUrl
}